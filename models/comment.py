from sqlalchemy import func

from db import db

user_liked_comments = db.Table("user_liked_comments",
                               db.Column("comment_id", db.Integer, db.ForeignKey("thread_comment.id")),
                               db.Column("user_id", db.Integer, db.ForeignKey("forum_users.id"))
                               )


class ThreadCommentModel(db.Model):
    __tablename__ = 'thread_comment'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)
    attachment = db.Column(db.String(300), nullable=True)
    created_on = db.Column(db.DateTime, nullable=False, server_default=func.now())
    users_liked = db.relationship("ForumUserModel", secondary=user_liked_comments, backref="liked_comments")
    forum_user_id = db.Column(db.Integer, db.ForeignKey("forum_users.id"), nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey("threads.id"), nullable=False)
