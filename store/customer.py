from flask import Flask, request, Response
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from configuration import Configuration
from models import database, Product, Category, ProductCategory, Order, OrderProduct
from sqlalchemy import and_
from role_check import role_check
import json
import datetime

application = Flask(__name__)
application.config.from_object(Configuration)
jwt = JWTManager(application)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def check_categories(product, cat):
    for category in product.categories:
        if cat in category.name:
            return True


@application.route("/search", methods=["GET"])
@jwt_required()
@role_check(role="customer")
def search():
    if "name" in request.args:
        name = request.args["name"]
    else:
        name = ""

    if "category" in request.args:
        category = request.args["category"]
    else:
        category = ""

    categories = Category.query.join(ProductCategory).join(Product).filter(
        and_(
            Category.name.like(f"%{category}%"),
            Product.name.like(f"%{name}%")
        )
    ).distinct(Category.name)

    categories = [category.name for category in categories]
    products = Product.query.filter(Product.name.like(f"%{name}%"))
    products = [product for product in products if check_categories(product, category)]

    products = [{
        "categories": [category.name for category in product.categories],
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    } for product in products]

    response = {
        "categories": categories,
        "products": products
    }

    return Response(json.dumps(response), status=200)


@application.route("/order", methods=["POST"])
@jwt_required()
@role_check(role="customer")
def order():
    if "requests" not in request.json:
        return Response(json.dumps({"message": "Field requests is missing."}), status=400)

    requests = request.json.get("requests")
    customer = get_jwt_identity()
    count = 0
    price = 0

    for req in requests:
        if "id" not in req:
            return Response(json.dumps({"message": f"Product id is missing for request number {count}."}), status=400)

        if "quantity" not in req:
            return Response(json.dumps({"message": f"Product quantity is missing for request number {count}."}), status=400)

        if not is_number(req["id"]) or req["id"] < 0:
            return Response(json.dumps({"message": f"Invalid product id for request number {count}."}), status=400)

        if not is_number(req["quantity"]) or req["quantity"] < 0:
            return Response(json.dumps({"message": f"Invalid product quantity for request number {count}."}), status=400)

        if Product.query.filter(Product.id == req["id"]).first() is None:
            return Response(json.dumps({"message": f"Invalid product for request number {count}."}), status=400)

        price += Product.query.filter(Product.id == req["id"]).first().price * req["quantity"]
        count = count + 1

    new_order = Order(price=price, status="COMPLETE", timestamp=datetime.datetime.now().isoformat(), customer=customer)
    database.session.add(new_order)
    database.session.commit()
    pending = False

    for req in requests:
        product = Product.query.filter(Product.id == req["id"]).first()
        quantity = req["quantity"]

        if product.quantity >= quantity:
            order_product = OrderProduct(order_id=new_order.id, product_id=product.id, received=quantity, requested=quantity, price=product.price)
            database.session.add(order_product)
            product.quantity -= quantity
            database.session.commit()
        else:
            order_product = OrderProduct(order_id=new_order.id, product_id=product.id, received=product.quantity, requested=quantity, price=product.price)
            database.session.add(order_product)
            product.quantity = 0
            database.session.commit()
            pending = True

    if pending:
        new_order.status = "PENDING"
        database.session.commit()

    return Response(json.dumps({"id": new_order.id}), 200)


@application.route("/status", methods=["GET"])
@jwt_required()
@role_check(role="customer")
def status():
    customer = get_jwt_identity()
    orders = Order.query.filter(Order.customer == customer).all()

    orders = [{
        "products": [{
            "categories": [category.name for category in product.categories],
            "name": product.name,
            "price": OrderProduct.query.filter(OrderProduct.order_id == curr_order.id, OrderProduct.product_id == product.id).first().price,
            "received": OrderProduct.query.filter(OrderProduct.order_id == curr_order.id, OrderProduct.product_id == product.id).first().received,
            "requested": OrderProduct.query.filter(OrderProduct.order_id == curr_order.id, OrderProduct.product_id == product.id).first().requested,
        } for product in curr_order.products],
        "price": curr_order.price,
        "status": curr_order.status,
        "timestamp": curr_order.timestamp
    } for curr_order in orders]

    return Response(json.dumps({"orders": orders}), 200)


if __name__ == "__main__":
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5002)
