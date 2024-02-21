from app.extensions import db


class ItemModel(db.Model):
    __tablename__="items"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(80), unique = False, nullable=False)
    price = db.Column(db.Float, unique = False, nullable =False)


    # Foreign key to represent the store the item belongs to
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)

    # Relationship to represent the store (many-to-one, as one item belongs to one store)
    store = db.relationship("StoreModel", back_populates="items")


class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    # Foreign key to represent the owner of the store
    # owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    #
    # # Relationship to represent the owner (one-to-many, as one user can own many stores)
    # owner = db.relationship("UserModel", back_populates="stores_owned", foreign_keys=[owner_id])

    # Relationship to represent the items in the store (one-to-many, as one store can have many items)
    items = db.relationship("ItemModel", back_populates="store", cascade="all, delete-orphan")


class MessageModel(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message_id = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))
    show = db.Column(db.Boolean(), default=0)
    duration = db.Column(db.Integer, default=5)
    status = db.Column(db.String(20), default='success')
    message = db.Column(db.String(500), nullable=False)
    dynamic = db.Column(db.Boolean(), default=0)
    object = db.Column(db.String(255))

class PermissionsModel(db.Model):
    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    permissionsApi = db.Column(db.String(80), nullable=False)


class RolePermission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey("permissions.id"), nullable=False)


class RoleModel(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rolename = db.Column(db.String(40), nullable=False)
    slug = db.Column(db.String(40), nullable=False, unique=True)
    groups = db.relationship("GroupModel", back_populates="roles", secondary="GroupRole")


class GroupRole(db.Model):
    __tablename__ = "GroupRole"
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)


class GroupModel(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    groupname = db.Column(db.String(80), nullable=False)
    roles = db.relationship("RoleModel", back_populates="groups", secondary="GroupRole")
    users = db.relationship("UserModel", back_populates="group", lazy="dynamic")


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, unique=False)

    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    group = db.relationship("GroupModel", back_populates="users")

    def getPassword(self):
        return self.password

    def has_role(self, role):
        return bool(
            RoleModel.query
            .join(RoleModel.users)
            .filter(UserModel.id == self.id)
            .filter(RoleModel.slug == role)
            .count() == 1
        )
