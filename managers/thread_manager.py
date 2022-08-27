import os
import uuid

from werkzeug.exceptions import NotAcceptable, Unauthorized, NotFound, BadRequest

from constants import TEMP_FILE_FOLDER
from db import db
from managers.auth import auth
from models import ThreadModel
from schemas.responses.thread import ThreadSchemaResponse
from services.s3 import S3Service
from utils.helpers import decode_file


class ThreadManager:
    @staticmethod
    def get_thread(thread_id):
        queried_thread = ThreadModel.query.filter_by(id=thread_id).first()
        if queried_thread:
            return queried_thread
        raise NotFound("No thread found with this ID!")

    @staticmethod
    def get_all_threads():
        all_threads_query = ThreadModel.query.all()
        if all_threads_query:
            return ThreadSchemaResponse(many=True).dump(all_threads_query)
        else:
            return "No threads created!"

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
                thread_data["attachment"] = attachment_url
                thread = ThreadModel(**thread_data)
                db.session.add(thread)
                db.session.flush()
                return thread

            except Exception:
                s3.remove_attachment(file_name)
                raise BadRequest("Problems with submitted data !")
            finally:
                os.remove(path)

        elif "attachment" in thread_data and "attachment_extension" not in thread_data:
            raise BadRequest("Please make sure to include both attachment and attachment extension if you want to "
                             "attach a file!")

        elif "attachment" not in thread_data and "attachment_extension" in thread_data:
            raise BadRequest("Please make sure to include both attachment and attachment extension if you want to "
                             "attach a file!")
        else:
            thread = ThreadModel(**thread_data)
            db.session.add(thread)
            db.session.flush()
            return thread

    @staticmethod
    def delete_thread(thread_id):
        thread = ThreadModel.query.filter_by(id=thread_id).first()
        if thread:
            db.session.delete(thread)
            db.session.flush()
            return "Thread deleted!"
        raise NotFound("No thread found with this ID!")

    @staticmethod
    def update_thread(thread_id, thread_data):
        current_user = auth.current_user()
        thread = ThreadModel.query.filter_by(id=thread_id).first()
        if thread and thread.forum_user_id == current_user:
            ThreadModel.query.filter_by(id=thread_id).update(thread_data)
            db.session.flush()
            return thread
        elif thread and thread.forum_user_id != current_user:
            raise Unauthorized("You are not the creator of the thread!")
        elif not thread:
            raise NotFound("No thread found with this ID!")

    @staticmethod
    def update_thread_status(thread_id, status):
        thread = ThreadModel.query.filter_by(id=thread_id).first()
        if thread and thread.status.value != status:
            thread_update_query = ThreadModel.query.filter_by(id=thread_id).update({"status": status})
            db.session.flush()
            return "Thread status was changed!"
        elif thread and thread.status.value == status:
            raise NotAcceptable("Thread in this status already!")
        elif not thread:
            raise NotFound("No thread found with this ID!")

    @staticmethod
    def thread_like_unlike(action, thread_id):
        user = auth.current_user()
        liked_threads = user.liked_threads
        action_change = "impossible"
        thread = ThreadModel.query.filter_by(id=thread_id).first()

        if action == "like" and thread and thread not in liked_threads:
            action_change = "possible"
            thread.likes += 1
            thread.users_liked.append(user)

        elif action == "dislike" and thread and thread in liked_threads:
            action_change = "possible"
            thread.likes -= 1
            thread.users_liked.remove(user)

        elif action_change == "impossible" and thread and action == "dislike":
            raise NotAcceptable("You have not liked this thread!")

        elif action_change == "impossible" and thread and action == "like":
            raise NotAcceptable("You have liked this already!")
        elif not thread:
            raise NotFound("No thread found with this ID!")

        db.session.flush()
        return thread
