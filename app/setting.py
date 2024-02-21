import os

os_env = os.environ


class Config(object):
    SECRET_KEY = "3nF3Rn0"
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_ENABLED = True  # Disable Debug toolbar
    TEMPLATES_AUTO_RELOAD = True
    HOST = '0.0.0.0'

    # version
    VERSION = "1"

    # JWT config
    JWT_SECRET_KEY = "127194167987254406973702788379750563935"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", 'refresh']

    # My sql config
    SQLALCHEMY_DATABASE_URI = 'mysql://root:XY58JqcxNLmy8SHN@192.168.1.17:3308/rbac?charset=utf8mb4'
    # My sql config
#    SQLALCHEMY_DATABASE_URI = 'mysql://root:tung1234567890@db:3306/rbac?charset=utf8mb4'

    # Redis config
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    # REDIS_DB = 2
    REDIS_PASSWORD = "tung1234567890"
