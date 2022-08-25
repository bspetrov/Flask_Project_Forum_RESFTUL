from marshmallow import fields

from schemas.base import CommentBase


class CommentSchemaRequest(CommentBase):
    attachment = fields.String(required=False)
