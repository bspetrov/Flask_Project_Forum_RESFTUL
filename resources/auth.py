from flask import request
from flask_api import status
from flask_restful import Resource

from managers.forum_manager import ForumManager
from managers.forum_user import ForumUserManager
from schemas.requests.auth import RegisterUserSchemaRequest, LoginUserSchemaRequest
from utils.decorators import validate_schema


class RegisterUserResource(Resource):
    @validate_schema(RegisterUserSchemaRequest)
    def post(self):
        data = request.get_json()
        token = ForumUserManager.register(data)
        return {"token": token, "message": "Forum user registered successfully!"}, status.HTTP_201_CREATED


class LoginUserResource(Resource):
    @validate_schema(LoginUserSchemaRequest)
    def post(self, type):
        data = request.get_json()
        if type == "forum_user":
            token = ForumUserManager.login(data)

        elif type == "manager":
            token = ForumManager.login(data)

        return {"token": token, "message": f"{type} in successfully!"}, status.HTTP_200_OK

