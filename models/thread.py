from sqlalchemy import func

from db import db
from models.enums import ThreadState


class ThreadModel(db.Model):
    __tablename__ = 'threads'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(ThreadState), default=ThreadState.open, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, server_default=func.now())
    likes = db.Column(db.Integer, nullable=False, default=0)
    comments = db.relationship("ThreadCommentModel", backref='thread_comment', lazy='dynamic')
    forum_user_id = db.Column(db.Integer, db.ForeignKey("forum_users.id"), nullable=False)
    forum_user = db.relationship("ForumUserModel")