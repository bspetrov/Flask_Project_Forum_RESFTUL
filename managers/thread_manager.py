import uuid
import os
from constants import TEMP_FILE_FOLDER
from db import db
from models import ThreadModel, ThreadCommentModel
from managers.auth import auth
from werkzeug.exceptions import NotAcceptable, Unauthorized, NotFound, InternalServerError

from schemas.responses.thread import ThreadSchemaResponse
from services.s3 import S3Service
from utils.helpers import decode_file


class ThreadManager:
    @staticmethod
    def get_thread(thread_id):
        queried_thread = ThreadModel.query.filter_by(id=thread_id).first()
        return queried_thread

    @staticmethod
    def get_all_threads():
        try:
            all_threads_query = ThreadModel.query.all()
            return ThreadSchemaResponse(many=True).dump(all_threads_query)
        except Exception as e:
            return e

    @staticmethod
    def create_thread(thread_data, user):
        thread_data["forum_user_id"] = user.id

        if "attachment" in thread_data and "attachment_extension" in thread_data:
            s3 = S3Service()
            file_name = f"{str(uuid.uuid4())}.{thread_data['attachment_extension']}"
            thread_data.pop("attachment_extension")
            path = os.path.join(TEMP_FILE_FOLDER, file_name)

            try:
                decode_file(path, thread_data["attachment"])
                attachment_url = s3.upload_attachment(path, file_name)
                thread_data["attachmentz"] = attachment_url
                thread = ThreadModel(**thread_data)
                db.session.add(thread)
                db.session.commit()
                return thread

            except Exception as e:
                s3.remove_attachment(file_name)
                raise InternalServerError("Problems with submitted data data!")

            finally:
                os.remove(path)

        elif "attachment" in thread_data and "attachment_extension" not in thread_data:
            raise NotAcceptable("Please make sure to include both attachment and attachment extension if you want to "
                                "attach a file!")

        elif "attachment" not in thread_data and "attachment_extension" in thread_data:
            raise NotAcceptable("Please make sure to include both attachment and attachment extension if you want to "
                                "attach a file!")
        else:
            thread = ThreadModel(**thread_data)
            db.session.add(thread)
            db.session.commit()

        return thread

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
        thread = ThreadModel.query.filter_by(id=thread_id).first()
        if thread.forum_user_id == current_user.id:
            ThreadModel.query.filter_by(id=thread_id).update(thread_data)
            db.session.commit()
            return thread
        else:
            raise Unauthorized("You are not the creator of the thread!")

    @staticmethod
    def update_thread_status(thread_id, status):
        thread = ThreadModel.query.filter_by(id=thread_id).first()
        if thread.status.value != status:
            thread_update_query = ThreadModel.query.filter_by(id=thread_id).update({"status": status})
            db.session.commit()
            return "Thread status was changed!"
        else:
            raise NotAcceptable("Thread in this status already!")

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

        elif action_change == "impossible" and action == "dislike":
            raise NotAcceptable("You have not liked this thread!")

        elif action_change == "impossible" and action == "like":
            raise NotAcceptable("You have liked this already!")

        db.session.commit()
        return thread

