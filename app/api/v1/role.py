from flask import request
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.model import RoleModel, UserModel
from app.gateway import auth_role
from app.utils import send_result, trim_dict

blp = Blueprint("Roles", __name__)


@blp.route("/change_role", methods=['POST'], endpoint='change_role')
@auth_role()
@jwt_required
def Change_role_user() -> dict:
    input_data = request.get_json()
    user_data = input_data.get("username")
    new_role_slug = input_data.get("new_role")  # Assuming it's the slug of the new role

    # Get the new role object
    new_role = RoleModel.query.filter(RoleModel.slug == new_role_slug).first()
    new_role_id = new_role.id
    # Get the user and their old role
    user = UserModel.query.filter(UserModel.username == user_data).first()
    old_role = user.role.rolename

    if user and new_role:
        # Change the role of that user
        user.role = new_role
        db.session.commit()
        return send_result(code=200,
                           message=f"Update successful for user {user_data} from role {old_role} to {new_role.rolename}")
    else:
        return send_result(code=500, message=f"The user or role not found{new_role} and {user}")


@blp.route("/add_new_role", methods=['POST'], endpoint='add_new_role')
@auth_role()
@jwt_required
def Add_new_role() -> dict :
    # check format of json data
    try:
        role_req = request.get_json()
    except Exception as e:
        return send_result(code=500, message="Invalid format json")

    role_data = trim_dict(role_req)
    try:
        new_role_name = role_data.get("rolename")
        new_slug = role_data.get("slug")
    except Exception as e:
        return send_result(code=500, message="Wrong input parameter")

    if RoleModel.query.filter(RoleModel.rolename == new_role_name):
        return send_result(code=500, message="this name already have")
    if RoleModel.query.filter(RoleModel.slug == new_slug):
        return send_result(code=500, message="this slug already have")

    new_role = RoleModel(
        rolename=new_role_name,
        slug=new_slug
    )
    try:
        db.session.add(new_role)
        db.session.commit()
    except Exception as e:
        return send_result(code=500, message="error at commit to data base")
