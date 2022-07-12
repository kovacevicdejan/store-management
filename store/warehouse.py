from flask import Flask, Response, request
from flask_jwt_extended import JWTManager, jwt_required
from configuration import Configuration
from redis import Redis
from role_check import role_check
import csv
import io
import json

application = Flask(__name__)
application.config.from_object(Configuration)
jwt = JWTManager(application)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


@application.route("/update", methods=["POST"])
@jwt_required()
@role_check(role="manager")
def update():
    if "file" not in request.files:
        return Response(json.dumps({"message": "Field file is missing."}), 400)

    content = request.files["file"].stream.read().decode("utf-8")
    stream = io.StringIO(content)
    reader = csv.reader(stream)
    products = []
    count = 0

    for row in reader:
        if len(row) != 4:
            return Response(json.dumps({"message": f"Incorrect number of values on line {count}."}), 400)

        if not is_number(row[2]) or int(row[2]) <= 0:
            return Response(json.dumps({"message": f"Incorrect quantity on line {count}."}), 400)

        if not is_number(row[3]) or float(row[3]) <= 0:
            return Response(json.dumps({"message": f"Incorrect price on line {count}."}), 400)

        count = count + 1
        categories = row[0].split("|")

        products.append({
            "categories": categories,
            "name": row[1],
            "quantity": int(row[2]),
            "price": float(row[3])
        })

    with Redis(host=Configuration.REDIS_HOST) as redis:
        for product in products:
            redis.rpush(Configuration.REDIS_PRODUCT_LIST, json.dumps(product))

    return Response(status=200)


if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0", port=5001)
