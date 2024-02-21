from flask import Blueprint, request
from flask_jwt_extended import jwt_required, JWTManager
from app.model import ItemModel, StoreModel
from app.gateway import auth_role
from app.schemas import ItemSchema
from app.utils import send_result


jwt = JWTManager()

blp=Blueprint("Items", __name__)
#
# @jwt.user_lookup_loader
# def user_loader_callback(jwt_header, jwt_payload):
#     user_id = jwt_payload['sub']
#     # Load user from the database using the user_id
#     user = UserModel.query.get(user_id)
#
#     return user


@blp.route("/show_items", methods=['GET'], endpoint='show_items')
@auth_role()
@jwt_required
def Get_all_Items() -> dict:
    try:
        items = ItemModel.query.all()
        serialized_items = ItemSchema(many=True).dump(items)
        return send_result(data = serialized_items, code = 200, message="Show all items success")
    except Exception as e:
        return send_result(message="Error", code = 500)


# @blp.route("/change_items_in_store", methods=['POST'])
# @jwt_required()
# @auth_role(["owner"])
# def Change_item_in_store():
#     store = Sto



