from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from jwt import ExpiredSignatureError, InvalidTokenError
from werkzeug.exceptions import Unauthorized

from models import ForumUserModel


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {"sub": user.id, "exp": datetime.utcnow() + timedelta(minutes=180)}
        return jwt.encode(payload, key=config("JWT_SECRET"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        if not token:
            raise Unauthorized("Missing token!")
        try:
            payload = jwt.decode(token, key=config("JWT_SECRET"), algorithms=["HS256"])
            return payload["sub"]
        except ExpiredSignatureError:
            raise Unauthorized("Token expired!")
        except InvalidTokenError:
            raise Unauthorized("Invalid token")


auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    try:
        user_id = AuthManager.decode_token(token)
        return ForumUserModel.query.filter_by(id=user_id).first()
    except Exception:
        return 400