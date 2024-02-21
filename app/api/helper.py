import os
import pickle

from app.setting import DevConfig
from app.extensions import red
from flask_jwt_extended import decode_token
from datetime import datetime
from app.model import PermissionsModel, GroupRole, RolePermission

CONFIG = DevConfig if os.environ.get('ENV') == 'prd' else DevConfig if os.environ.get('ENV') == 'stg' else DevConfig


class Token:
    @classmethod
    def add_token_to_database(cls, encoded_token: str, user_id: str):
        decoded_token = decode_token(encoded_token)
        jti = decoded_token['jti']
        expires = int((decoded_token['exp'] - int(datetime.now().timestamp())))
        if not jti or not expires:
            raise ValueError("Invalid token data")
        tokens_jti = red.get(user_id)
        tokens_jti = tokens_jti.decode() + ',' + jti if tokens_jti else jti
        red.set(user_id, tokens_jti)
        red.set(jti, encoded_token, expires)

    @classmethod
    def revoke_all_token(cls, user_id: str):
        tokens_jti = red.get(user_id)  # trả về kiểu bytes nên ta cần decode() để đổi về chuỗi
        tokens_jti = tokens_jti.decode() if tokens_jti else ''
        tokens_jti = tokens_jti.split(',')
        for jti in tokens_jti:
            red.delete(jti)
        red.set(user_id, '')

    @classmethod
    def revoke_token(cls, jti):
        red.delete(jti)

    @classmethod
    def add_list_permission(cls, user_id, list_permission: list):
        permission_user = f"permission_{user_id}"
        red.set(permission_user, pickle.dumps(list_permission))
        print(pickle.dumps(list_permission))
        list_result = pickle.loads(pickle.dumps(list_permission))
        for list in list_result:
            print(list)

    @classmethod
    def get_list_permission(cls, user) -> list:
        permissions = []
        group = user.group_id
        list_role = GroupRole.query.filter(GroupRole.group_id == group).all()
        for group_role in list_role:
            list_permission = RolePermission.query.filter(RolePermission.role_id == group_role.role_id).all()
            for role_permission in list_permission:
                permission = PermissionsModel.query.filter(PermissionsModel.id == role_permission.permission_id).first()
                if permission.permissionsApi not in permissions:
                    permissions.append(permission.permissionsApi)

        return permissions

    @classmethod
    def revoke_permission(cls, user):
        permission_user = f"permission_{user.id}"
        red.delete(permission_user)
