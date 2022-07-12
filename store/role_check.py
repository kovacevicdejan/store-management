from flask import Response
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
import json


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
