from schemas.base import CommentBase
from marshmallow import fields


class CommentSchemaResponse(CommentBase):
    id = fields.Int(required=True)
    created_on = fields.DateTime(required=True)
    thread = fields.String(required=True)
