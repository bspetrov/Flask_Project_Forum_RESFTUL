from marshmallow import fields

from schemas.base import ThreadBase


class ThreadSchemaRequest(ThreadBase):
    attachment = fields.String(required=False, default=None)
    attachment_extension = fields.String(required=False, default=None)
