from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField

from models import ThreadCategories


class AuthBase(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8, max=20))


class ThreadBase(Schema):
    title = fields.Str(required=True)
    category = EnumField(ThreadCategories, by_value=True)
    description = fields.Str(required=True)