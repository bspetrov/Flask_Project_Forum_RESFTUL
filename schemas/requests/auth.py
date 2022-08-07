from marshmallow import fields, Schema, validate

from schemas.base import AuthBase


class RegisterUserSchemaRequest(AuthBase):
    first_name = fields.Str(required=True, validate=validate.Length(min=2, max=20))
    last_name = fields.Str(required=True, validate=validate.Length(min=2, max=20))
    email = fields.Email(required=True)


class LoginUserSchemaRequest(AuthBase):
    pass
