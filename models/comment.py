from db import db


class ThreadCommentModel(db.Model):
    __tablename__ = 'thread_comment'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)
    forum_user_id = db.Column(db.Integer, db.ForeignKey("forum_users.id"), nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey("threads.id"), nullable=False)