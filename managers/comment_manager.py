from werkzeug.exceptions import Unauthorized, NotFound, NotAcceptable

from db import db
from managers.auth import auth
from models import ThreadCommentModel, ThreadModel
from schemas.responses.comment import CommentSchemaResponse


class CommentManager:
    @staticmethod
    def get_comment(data_id):
        comment_query = ThreadCommentModel.query.filter_by(id=data_id).first()
        if comment_query:
            return comment_query
        else:
            raise NotFound("No thread found with this ID!")

    @staticmethod
    def get_all_comments(thread_id):
        all_comments_query = ThreadCommentModel.query.filter_by(thread_id=thread_id).all()
        if all_comments_query:
            return CommentSchemaResponse(many=True).dump(all_comments_query)
        else:
            return "No comments available!"

    @staticmethod
    def comment_thread(comment_data):
        thread_model = ThreadModel.query.filter_by(id=comment_data["thread_id"]).first()
        if thread_model:
            comment_model = ThreadCommentModel(**comment_data)
            thread_model.comments.append(comment_model)
            db.session.add(comment_model)
            db.session.flush()
            return thread_model
        raise NotFound("No thread found with this ID!")

    @staticmethod
    def delete_comment(comment_id):
        current_user = auth.current_user()
        comment = ThreadCommentModel.query.filter_by(id=comment_id).first()
        if comment and comment.forum_user_id == current_user.id:
            comment_model = ThreadCommentModel.query.filter_by(id=comment_id).first()
            db.session.delete(comment_model)
            db.session.flush()
            return "Comment has been deleted!"
        elif comment and comment.forum_user_id != current_user.id:
            raise Unauthorized("Only the comment creator can delete his comments!")
        elif not comment:
            raise NotFound("No comment with this ID!")

    @staticmethod
    def edit_comment(comment_data, comment_id):
        current_user = auth.current_user()
        comment = ThreadCommentModel.query.filter_by(id=comment_id).first()
        if comment and comment.forum_user_id == current_user.id:
            ThreadCommentModel.query.filter_by(id=comment_id).update(comment_data)
            db.session.flush()
            return comment
        elif comment and comment.forum_user_id != current_user.id:
            raise Unauthorized("You are not the creator of the thread!")
        elif not comment:
            raise NotFound("No comment with this ID!")

    @staticmethod
    def like_dislike_comment(action, comment_id):
        user = auth.current_user()
        liked_comments = user.liked_comments
        action_change = "impossible"
        comment = ThreadCommentModel.query.filter_by(id=comment_id).first()

        if comment and action == "like" and comment not in liked_comments:
            action_change = "possible"
            comment.likes += 1
            comment.users_liked.append(user)

        elif comment and action == "dislike" and comment in liked_comments:
            action_change = "possible"
            comment.likes -= 1
            comment.users_liked.remove(user)

        elif comment and action_change == "impossible" and action == "dislike":
            raise NotAcceptable("You have not liked this comment!")

        elif comment and action_change == "impossible" and action == "like":
            raise NotAcceptable("You have liked this already!")

        elif not comment:
            raise NotFound("No comment with this ID!")

        db.session.flush()
        return comment
