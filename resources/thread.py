from flask import request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import Unauthorized, NotAcceptable


from managers.auth import auth
from managers.comment_manager import CommentManager
from managers.thread_manager import ThreadManager
from models import UserRole
from schemas.requests.comment import CommentSchemaRequest
from schemas.requests.thread import ThreadSchemaRequest
from schemas.responses.comment import CommentSchemaResponse
from schemas.responses.thread import ThreadSchemaResponse
from utils.decorators import validate_schema, permission_required


class MainThreadResource(Resource):
    """
    Gets all threads!
    """
    def get(self):
        threads = ThreadManager.get_all_threads()
        return {"threads": threads}, status.HTTP_200_OK

    """
    Creates a thread, must be authenticated!
    """
    @auth.login_required
    @validate_schema(ThreadSchemaRequest)
    def post(self):
        data = request.get_json()
        current_user = auth.current_user()
        new_thread = ThreadManager.create_thread(data, current_user)
        return ThreadSchemaResponse().dump(new_thread), status.HTTP_201_CREATED


class SingleThreadActionResource(Resource):
    """
    Gets a single thread with all its comments!
    """
    @auth.login_required
    def get(self,  action, id):
        if action == "get":
            try:
                thread = ThreadManager.get_thread(id)
                comments = CommentManager.get_all_comments(id)
                return {
                    "thread": ThreadSchemaResponse().dump(thread),
                    "comments": comments
                }
            except Exception:
                return status.HTTP_404_NOT_FOUND
        else:
            raise NotAcceptable(f"Action {action} is not acceptable!")

    """
    Submits a comment for the thread!
    """
    @auth.login_required
    @validate_schema(CommentSchemaRequest)
    def post(self, action, id):
        if action == "comment":
            data = request.get_json()
            current_user = auth.current_user()
            data["thread_id"] = id
            data["forum_user_id"] = current_user.id
            commented_thread = CommentManager.comment_thread(data)
            comments = CommentManager.get_all_comments(id)
            return {
                "thread": ThreadSchemaResponse().dump(commented_thread),
                "comments": comments
            }
        else:
            raise NotAcceptable(f"Action {action} is not acceptable!")

    "This put method is used to like, dislike, update thread data"
    @auth.login_required
    def put(self, action, id):
        if action == "like" or action == "dislike":
            liked_thread = ThreadManager.thread_like_unlike(action, id)
            return ThreadSchemaResponse().dump(liked_thread), status.HTTP_200_OK

        elif action == "update-data":
            data = request.get_json()
            updated_thread = ThreadManager.update_thread(id, data)
            return ThreadSchemaResponse().dump(updated_thread), status.HTTP_200_OK
        else:
            raise NotAcceptable(f"Action {action} is not acceptable!")

    @auth.login_required
    @permission_required(UserRole.manager)
    def delete(self, action, id):
        if action == "delete":
            delete_thread = ThreadManager.delete_thread(id)
            return {"message": delete_thread}
        else:
            raise NotAcceptable(f"Action {action} is not acceptable!")


class ManagerThreadActionResource(Resource):
    @auth.login_required
    @permission_required(UserRole.manager)
    def put(self, action, id):
        if action == "update-status":
            data = request.get_json()
            status = data["status"]
            modified_thread = ThreadManager.update_thread_status(id, status)
            return modified_thread
        else:
            raise NotAcceptable(f"Action {action} is not acceptable!")




