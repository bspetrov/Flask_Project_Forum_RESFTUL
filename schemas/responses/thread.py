from marshmallow import fields
from marshmallow_enum import EnumField

from models import ThreadState
from schemas.base import ThreadBase


class ThreadSchemaResponse(ThreadBase):
    id = fields.Int(required=True)
    created_on = fields.DateTime(required=True)
    thread_status = EnumField(ThreadState, by_value=True)

