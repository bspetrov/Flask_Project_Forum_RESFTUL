from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash

from managers.auth import AuthManager
from models import ForumManagerModel


class ForumManager:
    @staticmethod
    def login(data):
        """
        This manager class is used to query and login a Forum Manager!
        :param data:
        :return: JWT Token!
        """
        manager = ForumManagerModel.query.filter_by(username=data["username"]).first()
        if not manager:
            raise BadRequest("Manager doesn't exist!")

        if check_password_hash(manager.password, data["password"]):
            return AuthManager.encode_token(manager)
        raise BadRequest("Invalid credentials!")
