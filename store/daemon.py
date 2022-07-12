from flask import Flask
from redis.client import Redis
from configuration import Configuration
from models import database, Product, Category, ProductCategory, Order, OrderProduct
import json

application = Flask(__name__)
application.config.from_object(Configuration)


def check_categories(categories1, categories2):
    for curr_category in categories1:
        if curr_category not in categories2:
            return False

    return True


if __name__ == "__main__":
    database.init_app(application)

    try:
        while True:
            with Redis(host=Configuration.REDIS_HOST) as redis:
                with application.app_context():
                    redis_bytes = redis.blpop(Configuration.REDIS_PRODUCT_LIST)
                    product = json.loads(redis_bytes[1])

                    if Product.query.filter(Product.name == product["name"]).first() is None:
                        categories = product["categories"]
                        product = Product(name=product["name"], price=product["price"], quantity=product["quantity"])
                        database.session.add(product)
                        database.session.commit()

                        for name in categories:
                            if Category.query.filter(Category.name == name).first() is None:
                                category = Category(name=name)
                                database.session.add(category)
                                database.session.commit()
                            else:
                                category = Category.query.filter(Category.name == name).first()

                            product_category = ProductCategory(product_id=product.id, category_id=category.id)
                            database.session.add(product_category)
                            database.session.commit()
                    else:
                        categories = product["categories"]
                        price = product["price"]
                        quantity = product["quantity"]
                        product = Product.query.filter(Product.name == product["name"]).first()
                        product_categories = [category.name for category in product.categories]

                        if check_categories(categories, product_categories):
                            new_price = (product.quantity * product.price + price * quantity) / (
                                        product.quantity + quantity)
                            product.price = new_price
                            product.quantity += quantity
                            database.session.commit()

                        order_products = OrderProduct.query.filter(OrderProduct.product_id == product.id, OrderProduct.requested != OrderProduct.received).all()

                        for order_product in order_products:
                            if product.quantity >= order_product.requested - order_product.received:
                                product.quantity = product.quantity - order_product.requested + order_product.received
                                order_product.received = order_product.requested
                                database.session.commit()
                                pending = OrderProduct.query.filter(OrderProduct.order_id == order_product.order_id, OrderProduct.requested != OrderProduct.received).first()

                                if pending is None:
                                    order = Order.query.filter(Order.id == order_product.order_id).first()
                                    order.status = "COMPLETE"
                                    database.session.commit()
                            else:
                                order_product.received += product.quantity
                                product.quantity = 0
                                database.session.commit()
                                break
    except Exception as error:
        print(error)
