from marshmallow import fields
from marshmallow_enum import EnumField

from models import ThreadState, ThreadCategories
from schemas.base import ThreadBase, CommentBase


class ThreadSchemaResponse(ThreadBase):
    id = fields.Int(required=True)
    likes = fields.Int(required=True)
    created_on = fields.DateTime(required=True)
    status = EnumField(ThreadState, by_value=True)
    attachment = fields.URL(required=True)



