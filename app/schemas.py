from marshmallow import Schema, fields
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name= fields.String(required=True)
    price = fields.Float(required=True)



class MessageSchema(Schema):
    id = fields.Integer(required=True)
    message_id = fields.String(required=True)
    description = fields.String()
    show = fields.Boolean(default=False)
    duration = fields.Integer(default=5)
    status = fields.String(default='success')
    message = fields.String(required=True)
    dynamic = fields.Boolean(default=False)
    object = fields.String()
