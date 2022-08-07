from marshmallow import Schema, fields, validate


class AuthBase(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8, max=20))


class ThreadBase(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
