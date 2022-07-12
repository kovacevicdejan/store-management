from flask import Flask, request, Response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, create_refresh_token, get_jwt, \
    get_jwt_identity, verify_jwt_in_request
from configuration import Configuration
from models import database, User, Role, UserRole
from sqlalchemy import and_
from functools import wraps
import json
import re

application = Flask(__name__)
application.config.from_object(Configuration)
jwt = JWTManager(application)


def role_check(role):
    def inner_role_check(function):
        @wraps(function)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            if 'roles' in claims and role in claims['roles']:
                return function(*args, **kwargs)
            else:
                return Response(json.dumps({"msg": "Missing Authorization Header"}), status=401)

        return decorator

    return inner_role_check


@application.route("/register", methods=["POST"])
def register():
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    forename = request.json.get("forename", "")
    surname = request.json.get("surname", "")
    is_customer = request.json.get("isCustomer", "")

    email_empty = len(email) == 0
    password_empty = len(password) == 0
    forename_empty = len(forename) == 0
    surname_empty = len(surname) == 0
    is_customer_empty = len(str(is_customer)) == 0

    if forename_empty:
        return Response(json.dumps({"message": "Field forename is missing."}), 400)

    if surname_empty:
        return Response(json.dumps({"message": "Field surname is missing."}), 400)

    if email_empty:
        return Response(json.dumps({"message": "Field email is missing."}), 400)

    if password_empty:
        return Response(json.dumps({"message": "Field password is missing."}), 400)

    if is_customer_empty:
        return Response(json.dumps({"message": "Field isCustomer is missing."}), 400)

    if len(email) > 256 or not re.fullmatch(r"[^@]+@[^@]+\.[^@]{2,}", email):
        return Response(json.dumps({"message": "Invalid email."}), 400)

    if len(password) < 8 or len(password) > 256 or not re.search(r"\d", password) or not re.search(r"[a-z]", password) or not re.search(r"[A-Z]", password):
        return Response(json.dumps({"message": "Invalid password."}), 400)

    user = User.query.filter(User.email == email).first()

    if user:
        return Response(json.dumps({"message": "Email already exists."}), 400)

    user = User(email=email, password=password, forename=forename, surname=surname)
    database.session.add(user)
    database.session.commit()

    if is_customer:
        role_id = Role.query.filter(Role.name == "customer").first().id
    else:
        role_id = Role.query.filter(Role.name == "manager").first().id

    user_role = UserRole(user_id=user.id, role_id=role_id)
    database.session.add(user_role)
    database.session.commit()

    return Response("Registration successful!", status=200)


@application.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    email_empty = len(email) == 0
    password_empty = len(password) == 0

    if email_empty:
        return Response(json.dumps({"message": "Field email is missing."}), 400)

    if password_empty:
        return Response(json.dumps({"message": "Field password is missing."}), 400)

    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]{2,}", email):
        return Response(json.dumps({"message": "Invalid email."}), 400)

    user = User.query.filter(and_(User.email == email, User.password == password)).first()

    if not user:
        return Response(json.dumps({"message": "Invalid credentials."}), 400)

    additional_claims = {
        "forename": user.forename,
        "surname": user.surname,
        "roles": [str(role.name) for role in user.roles]
    }

    access_token = create_access_token(identity=user.email, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=user.email, additional_claims=additional_claims)
    return Response(json.dumps({"accessToken": access_token, "refreshToken": refresh_token}), 200)


@application.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    refresh_claims = get_jwt()

    additional_claims = {
        "forename": refresh_claims["forename"],
        "surname": refresh_claims["surname"],
        "roles": refresh_claims["roles"]
    }

    access_token = create_access_token(identity=identity, additional_claims=additional_claims)
    return Response(json.dumps({"accessToken": access_token}), 200)


@application.route("/delete", methods=["POST"])
@jwt_required()
@role_check(role='admin')
def delete():
    email = request.json.get("email", "")
    email_empty = len(email) == 0

    if email_empty:
        return Response(json.dumps({"message": "Field email is missing."}), 400)

    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]{2,}", email):
        return Response(json.dumps({"message": "Invalid email."}), 400)

    user = User.query.filter(User.email == email).first()

    if not user:
        return Response(json.dumps({"message": "Unknown user."}), 400)

    database.session.delete(user)
    database.session.commit()
    return Response(status=200)


if __name__ == "__main__":
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5000)
