from flask import request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import NotAcceptable

from managers.auth import auth
from managers.comment_manager import CommentManager
from schemas.requests.comment import CommentSchemaRequest
from schemas.responses.comment import CommentSchemaResponse
from schemas.responses.thread import ThreadSchemaResponse
from utils.decorators import validate_schema


class SingleCommentResource(Resource):
    @auth.login_required
    def get(self, action, id):
        if action == "get":
            comment_query = CommentManager.get_comment(id)
            return CommentSchemaResponse().dump(comment_query)
        else:
            raise NotAcceptable(f"Action {action} is not acceptable!")

    @auth.login_required
    def put(self, action, id):
        if action == "edit":
            data = request.get_json()
            comment_query = CommentManager.edit_comment(data, id)
            return CommentSchemaResponse().dump(comment_query)

        elif action == "like" or action == "dislike":
            comment_query = CommentManager.like_dislike_comment(action, id)
            return CommentSchemaResponse().dump(comment_query), status.HTTP_200_OK

    @auth.login_required
    def delete(self, action, id):
        if action == "delete":
            comment_query = CommentManager.delete_comment(id)
            return {"message": comment_query}
        else:
            raise NotAcceptable(f"Action {action} is not acceptable!")
