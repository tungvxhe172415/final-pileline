from flask import Flask
from app.api import v1 as api_v1
from app.extensions import jwt, db, red, migrate
from app.api.helper import CONFIG
from app.utils import send_result
from app.model import MessageModel
import json


def create_app(config_object=CONFIG):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_monitor(app)
    register_blueprints(app)
    with app.app_context():
        upload_messages_to_redis()

    return app


def register_extensions(app):
    db.app = app
    db.init_app(app)
    jwt.init_app(app)
    red.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(api_v1.user.blp, url_prefix='/api/v1/user')
    app.register_blueprint(api_v1.item.blp, url_prefix='/api/v1/item')
    app.register_blueprint(api_v1.role.blp, url_prefix='/api/v1/role')


def register_monitor(app):
    def has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)

    @app.route("/api/v1/helper/site-map", methods=['GET'])
    def site_map():
        links = []
        for rule in app.url_map.iter_rules():
            # Filter out rules we can't navigate to in a browser
            # and rules that require parameters
            # if has_no_empty_params(rule):

            # url = url_for(rule.endpoint, **(rule.defaults or {}))
            request_method = ""
            if "GET" in rule.methods:
                request_method = "get"
            if "PUT" in rule.methods:
                request_method = "put"
            if "POST" in rule.methods:
                request_method = "post"
            if "DELETE" in rule.methods:
                request_method = "delete"
            permission_route = "{0}@{1}".format(request_method.lower(), rule)
            links.append(permission_route)
        return send_result(data=sorted(links, key=lambda resource: str(resource).split('@')[-1]))

# add all data on  messenger on to redis

def upload_messages_to_redis():
    # Retrieve all messages from the Message table
    messages = MessageModel.query.all()

    # Store each message in Redis
    for message in messages:
        redis_key = f"message:{message.message_id}"  # Adjust the key as needed
        message_json = json.dumps({
            "message_id": message.message_id,
            "description": message.description,
            "show": message.show,
            "duration": message.duration,
            "status": message.status,
            "message": message.message,
            "dynamic": message.dynamic,
            "object": message.object
        })

        red.set(redis_key,message_json )


def upload_permissions_to_redis():
    pass
