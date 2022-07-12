from flask import Flask, Response
from flask_jwt_extended import JWTManager, jwt_required
from configuration import Configuration
from models import database, Product, Category, ProductCategory, OrderProduct
from sqlalchemy import func
from role_check import role_check
import json

application = Flask(__name__)
application.config.from_object(Configuration)
jwt = JWTManager(application)


@application.route("/productStatistics", methods=["GET"])
@jwt_required()
@role_check(role="admin")
def product_statistics():
    statistics = Product.query.join(OrderProduct).group_by(Product.name).with_entities(Product.name, func.sum(OrderProduct.requested).label("sold"), func.sum(OrderProduct.requested - OrderProduct.received).label("waiting"))

    statistics = [{
        "name": product.name,
        "sold": int(product.sold),
        "waiting": int(product.waiting)
    } for product in statistics]

    return Response(json.dumps({"statistics": statistics}), status=200)


@application.route("/categoryStatistics", methods=["GET"])
@jwt_required()
@role_check(role="admin")
def category_statistics():
    statistics = Category.query.outerjoin(ProductCategory).outerjoin(OrderProduct, ProductCategory.product_id == OrderProduct.product_id).group_by(Category.name).order_by(func.sum(func.coalesce(OrderProduct.requested, 0)).desc(), Category.name).with_entities(Category.name).all()
    statistics = [category.name for category in statistics]
    return Response(json.dumps({"statistics": statistics}), status=200)


if __name__ == "__main__":
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5003)
