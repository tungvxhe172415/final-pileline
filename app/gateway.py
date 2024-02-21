from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
import pickle
from app.extensions import red
from flask import request
from app.utils import send_result

jwt = JWTManager()


def auth_role():
    def wrapper(func):
        def decorator(*arg, **kwarg):
            verify_jwt_in_request()
            permission_route = "{0}@{1}".format(request.method.lower(), request.url_rule.rule)
            list_permission = pickle.loads(red.get(f"permission_{get_jwt_identity()}"))
            if permission_route in list_permission:
                return func(*arg, **kwarg)
            else:
                return send_result(code=500, message="Error")

        wrapper.__name__ = func.__name__
        return decorator

    return wrapper
