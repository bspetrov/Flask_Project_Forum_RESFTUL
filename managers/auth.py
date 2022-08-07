from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from jwt import ExpiredSignatureError, InvalidTokenError
from werkzeug.exceptions import Unauthorized


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


auth = HTTPTokenAuth()


@auth.verify_token
def verify(token):
    try:
        user_id, user_type = AuthManager.decode_token(token)
        return eval(f"{user_type}.query.filter_by(id={user_id}).first()")
    except Exception as ex:
        raise Unauthorized("Invalid or missing token")
