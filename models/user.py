from db import db
from models.enums import UserRole


class MainUserModel(db.Model):
    __abstract__ = True

    __tablename__ = 'main_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(75), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)


class ForumUserModel(MainUserModel):
    __tablename__ = "forum_users"

    threads = db.relationship("ThreadModel", backref="thread", lazy="dynamic")
    role = db.Column(db.Enum(UserRole), default=UserRole.simple_user, nullable=False)


class ForumManagerModel(MainUserModel):
    __tablename__ = 'forum_managers'

    role = db.Column(db.Enum(UserRole), default=UserRole.manager, nullable=False)
