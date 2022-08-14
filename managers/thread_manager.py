from db import db
from models import ThreadModel
from managers.auth import auth
from werkzeug.exceptions import NotAcceptable


class ThreadManager:
    @staticmethod
    def get_thread(thread_id):
        queried_thread = ThreadModel.query.filter_by(id=thread_id).first()
        return queried_thread

    @staticmethod
    def get_all_threads(user):
        user_threads = ThreadModel.query.filter_by(forum_user_id=user).all()
        return user_threads

    @staticmethod
    def create_thread(thread_data, user):
        thread_data["forum_user_id"] = user.id

        try:
            thread = ThreadModel(**thread_data)
            db.session.add(thread)
            db.session.commit()

            return thread

        except Exception as e:
            return e

    @staticmethod
    def update_thread(thread_id, thread_data):

        try:
            thread_update_query = ThreadModel.query.filter_by(id=thread_id).update(thread_data)
            db.session.commit()
            thread = ThreadModel.query.filter_by(id=thread_id).first()
            return thread

        except Exception as e:
            return e

    @staticmethod
    def update_thread_status(thread_id, status):

        try:
            thread_update_query = ThreadModel.query.filter_by(id=thread_id).update({"status": status})
            db.session.commit()
            return "Thread status was changed!"
        except Exception as e:
            return e

    @staticmethod
    def thread_like_unlike(action, thread_id):
        user = auth.current_user()
        liked_threads = user.liked_threads
        action_change = "impossible"
        thread = ThreadModel.query.filter_by(id=thread_id).first()

        if action == "like" and thread not in liked_threads:
            action_change = "possible"
            thread.likes += 1
            thread.users_liked.append(user)

        elif action == "dislike" and thread in liked_threads:
            action_change = "possible"
            thread.likes -= 1
            thread.users_liked.remove(user)

        if action_change == "impossible" and action == "dislike":
            raise NotAcceptable("You have not liked this thread!")
        elif action_change == "impossible" and action == "like":
            raise NotAcceptable("You have liked this already!")

        db.session.commit()
        return thread



