from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth import AuthManager
from models.user import ForumUserModel


class ForumUserManager:
    @staticmethod
    def register(forum_user_data):
        """
        This method registers the regular forum user!
        :param forum_user_data: dict
        :return: Forum User Token
        """
        forum_user_data["password"] = generate_password_hash(forum_user_data["password"])
        user = ForumUserModel(**forum_user_data)
        db.session.add(user)
        db.session.commit()
        return AuthManager.encode_token(user)

    @staticmethod
    def login(login_data):
        """
        This method logs in the regular forum user!
        :param login_data: dict
        :return: Forum User Token
        """
        forum_user = ForumUserModel.query.filter_by(username=login_data["username"]).first()
        if not forum_user:
            raise BadRequest("No such username.. Please register!")

        if check_password_hash(forum_user.password, login_data["password"]):
            return AuthManager.encode_token(forum_user)
        raise BadRequest("Wrong password!")