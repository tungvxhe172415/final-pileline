from flask import request
from passlib.hash import pbkdf2_sha256
from flask import Blueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from app.extensions import db
from app.model import UserModel, RoleModel
from app.gateway import auth_role
from app.api.helper import Token
from app.utils import trim_dict, send_result

blp = Blueprint("Users", __name__)


@blp.route("/register_user", methods=['POST'], endpoint='register_user')
@auth_role()
@jwt_required
def register_user() -> dict:
    # Check input format (you may want to add more validation here)
    try:
        user_data_req = request.get_json()
    except Exception as e:
        return send_result(code=500, message="Invalid format json")

    # delete white space
    user_data = trim_dict(user_data_req)

    # Check if the username already exists
    if UserModel.query.filter(UserModel.username == user_data["username"]).first():
        abort(500, message="This username already exists")

    # Create a new user
    user = UserModel(
        username=user_data["username"],
        email=user_data["email"],
        password=pbkdf2_sha256.hash(user_data["password"]),
        group_id = user_data["group_id"]
    )

    db.session.add(user)
    db.session.commit()

    return send_result(code=200, message="Add items success")


@blp.route("/delete_user", methods=['POST'], endpoint='delete_user')
@auth_role()
@jwt_required
def Delete_User() -> dict:
    # check the form json
    try:
        user_req = request.get_json()["username"]
    except Exception as e:
        return send_result(code=500, message="Invalid format of json: " + str(e))
    # trim the data, white space
    user_data = trim_dict(user_req)

    username = user_data["username"]
    if UserModel.query.filter(UserModel.username == username).first():
        user_delete = UserModel.query.filter(UserModel.username == username).first()
        Token.revoke_all_token(user_delete.id)
        # remove the row have username = username
        db.session.delete(user_delete)
        db.session.commit()
        return {"Mess": "Delete Successful"}
    else:
        return {"Mess": "The username not exsist"}


@blp.route("/login", methods=['POST'], endpoint='login')
def login():
    permission_route = "{0}@{1}".format(request.method.lower(), request.url_rule.rule)
    print(permission_route)
    # check format input
    try:
        user_data_req = request.get_json()
    except Exception as e:
        return send_result(code=500, message="Invalid format of json: " + str(e))
    # Trim the body json
    user_data = trim_dict(user_data_req)
    # query
    user = UserModel.query.filter(
        UserModel.username == user_data["username"]
    ).first()


    list_permission = Token.get_list_permission(user)




    # create token JWT and save to redis
    if user and pbkdf2_sha256.verify(user_data["password"], user.password):
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        Token.add_token_to_database(access_token, user.id)
        Token.add_token_to_database(refresh_token, user.id)
        Token.add_list_permission(user.id,list_permission )

        # return send_result(message_id=1)
        return {"access_token": access_token,
                "refresh_token": refresh_token}, 200

    abort(401, message="Invalid credentials.")
