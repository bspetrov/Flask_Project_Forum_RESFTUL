from db import db
from models import ThreadModel, ThreadCommentModel
from managers.auth import auth
from werkzeug.exceptions import NotAcceptable, Unauthorized, NotFound

from schemas.responses.thread import ThreadSchemaResponse


class ThreadManager:
    @staticmethod
    def get_thread(thread_id):
        queried_thread = ThreadModel.query.filter_by(id=thread_id).first()
        return queried_thread

    @staticmethod
    def get_all_threads():
        all_threads = []
        try:
            all_threads_query = ThreadModel.query.all()
            for thread in all_threads_query:
                dict = ThreadSchemaResponse().dump(thread)
                all_threads.append(dict)
            return all_threads
        except Exception as e:
            return e

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
    def delete_thread(thread_id):

        try:
            thread = ThreadModel.query.filter_by(id=thread_id).first()
            db.session.delete(thread)
            db.session.commit()
            return "Thread deleted!"

        except Exception as e:
            raise NotFound("Couldn't allocate thread with this id")

    @staticmethod
    def update_thread(thread_id, thread_data):
        current_user = auth.current_user()
        try:
            thread = ThreadModel.query.filter_by(id=thread_id).first()
            if thread.forum_user_id == current_user.id:
                ThreadModel.query.filter_by(id=thread_id).update(thread_data)
                db.session.commit()
                return thread
            else:
                raise Unauthorized("You are not the creator of the thread!")
        except Exception:
            raise NotFound("Couldn't find thread with this ID!")

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