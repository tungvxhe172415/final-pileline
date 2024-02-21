import os

from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_redis import Redis
from .setting import DevConfig

# Dev config
CONFIG = DevConfig

# JWT
jwt = JWTManager()

# SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()

# Redis
red = Redis()
