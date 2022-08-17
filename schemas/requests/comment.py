from schemas.base import CommentBase
from marshmallow import fields


class CommentSchemaRequest(CommentBase):
    attachment = fields.String(required=False)
