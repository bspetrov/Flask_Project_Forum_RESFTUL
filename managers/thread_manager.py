from db import db
from models import ThreadModel


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
    def update_thread_status(thread_id):
        pass



