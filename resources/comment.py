from flask import request
from flask_api import status
from flask_restful import Resource
from managers.auth import auth
from managers.comment_manager import CommentManager
from schemas.responses.comment import CommentSchemaResponse


class MainCommentResource(Resource):
    @auth.login_required
    def get(self, id):
        comment_query = CommentManager.get_comment(id)
        return CommentSchemaResponse().dump(comment_query)

    @auth.login_required
    def delete(self, id):
        comment_query = CommentManager.delete_comment(id)
        return {"message": comment_query}

    @auth.login_required
    def put(self, id):
        data = request.get_json()
        comment_query = CommentManager.edit_comment(data, id)
        return CommentSchemaResponse().dump(comment_query)
