from sqlalchemy import func

from db import db
from models.enums import ThreadState, ThreadCategories

user_liked_threads = db.Table("user_liked_threads",
                              db.Column("thread_id", db.Integer, db.ForeignKey("threads.id")),
                              db.Column("user_id", db.Integer, db.ForeignKey("forum_users.id"))
                              )


class ThreadModel(db.Model):
    __tablename__ = 'threads'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    category = db.Column(db.Enum(ThreadCategories), nullable=False)
    description = db.Column(db.Text, nullable=False)
    attachment = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Enum(ThreadState), nullable=False, default=ThreadState.open)
    created_on = db.Column(db.DateTime, nullable=False, server_default=func.now())
    likes = db.Column(db.Integer, nullable=False, default=0)
    users_liked = db.relationship("ForumUserModel", secondary=user_liked_threads, backref="liked_threads")
    comments = db.relationship("ThreadCommentModel", backref='thread_comment', lazy='dynamic')
    forum_user_id = db.Column(db.Integer, db.ForeignKey("forum_users.id"), nullable=False)
