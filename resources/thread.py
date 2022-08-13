from flask import request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import Unauthorized


from managers.auth import auth
from managers.thread_manager import ThreadManager
from models import UserRole
from schemas.requests.thread import ThreadSchemaRequest
from schemas.responses.thread import ThreadSchemaResponse
from utils.decorators import validate_schema, permission_required


class SingleThreadResource(Resource):
    def get(self, id):
        try:
            thread = ThreadManager.get_thread(id)
            return ThreadSchemaResponse().dump(thread), status.HTTP_200_OK

        except Exception:
            return status.HTTP_404_NOT_FOUND


class AllThreadsResource(Resource):
    @auth.login_required
    def get(self):
        try:
            current_user = auth.current_user()
            thread = ThreadManager.get_all_threads(current_user.id)
            return ThreadSchemaResponse().dump(thread), status.HTTP_200_OK

        except Exception:
            return status.HTTP_404_NOT_FOUND


class CreateThreadResource(Resource):
    @auth.login_required
    @validate_schema(ThreadSchemaRequest)
    def post(self):
        data = request.get_json()
        current_user = auth.current_user()
        new_thread = ThreadManager.create_thread(data, current_user)
        return ThreadSchemaResponse().dump(new_thread), status.HTTP_201_CREATED


class UpdateThreadResource(Resource):
    @auth.login_required()
    def put(self, id):
        data = request.get_json()
        modified_thread = ThreadManager.update_thread(id, data)
        return ThreadSchemaResponse().dump(modified_thread), status.HTTP_200_OK

class UpdateThreadStatusResource(Resource):
    @auth.login_required
    @permission_required(UserRole.manager)
    def put(self, id):
        pass



