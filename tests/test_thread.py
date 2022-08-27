import os
from unittest.mock import patch

from flask_testing import TestCase

from config import create_app
from constants import TEMP_FILE_FOLDER
from db import db
from models import ThreadCategories, ThreadModel
from services.s3 import S3Service
from tests.factories import ForumUserFactory, ManagerUserFactory
from tests.helpers import generate_user_token, encoded_file, encoded_file_extension, mock_uuid

THREAD_ENDPOINTS = (
    ("/thread/get/1/", "get"),
    ("/thread/comment/1/", "post"),
    ("/thread/like/1/", "put"),
    ("/thread/dislike/1/", "put"),
    ("/thread/update-data/1/", "put"),
    ("/thread/delete/1/", "delete"),
)

class TestThread(TestCase):

    def create_app(self):
        return create_app("config.TestConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_thread_schema(self):
        threads = ThreadModel.query.all()
        assert len(threads) == 0

        url = "/thread/"
        user = ForumUserFactory()
        token = generate_user_token(user)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        data = {}
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        assert resp.json["message"] == {
            "title": ["Missing data for required field."],
            "category": ["Missing data for required field."],
            "description": ["Missing data for required field."]
        }
        threads = ThreadModel.query.all()
        assert len(threads) == 0

    def test_create_thread_without_attachment(self):
        url = "/thread/"
        user = ForumUserFactory()
        token = generate_user_token(user)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description",
        }

        resp = self.client.post(url, headers=headers, json=data)
        assert resp.status_code == 201
        resp = resp.json
        expected_resp = {
            "title": data['title'],
            "category": ThreadCategories.gaming.value,
            "description": data['description'],
            "likes": resp["likes"],
            "attachment": None,
            "id": resp["id"],
            "created_on": resp["created_on"],
            "status": resp["status"]
        }

        assert resp == expected_resp

    @patch("uuid.uuid4", mock_uuid)
    @patch.object(S3Service, "upload_attachment", return_value="my.s3.url")
    def test_create_thread_with_attachment(self, s3_mock):
        url = "/thread/"
        user = ForumUserFactory()
        token = generate_user_token(user)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description",
            "attachment": encoded_file,
            "attachment_extension": encoded_file_extension
        }

        resp = self.client.post(url, headers=headers, json=data)
        assert resp.status_code == 201
        resp = resp.json
        expected_resp = {
            "title": data['title'],
            "category": ThreadCategories.gaming.value,
            "description": data['description'],
            "attachment": s3_mock.return_value,
            "id": resp["id"],
            "created_on": resp["created_on"],
            "status": resp["status"],
            "likes": resp["likes"]
        }

        assert resp == expected_resp
        file_name = f"{str(mock_uuid())}.{encoded_file_extension}"
        path = os.path.join(TEMP_FILE_FOLDER, file_name)
        s3_mock.assert_called()
        s3_mock.assert_called_once_with(path, file_name)
        a = 5

    def test_create_thread_schema_with_missing_attachment_field(self):
        url = "/thread/"
        user = ForumUserFactory()
        token = generate_user_token(user)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description",
            "attachment_extension": encoded_file_extension
        }

        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        self.assertEqual(resp.json,
                         {"message": "Please make sure to include both attachment and attachment extension if you want "
                                     "to attach a file!"})

    def test_create_thread_schema_with_missing_attachment_extension_field(self):
        url = "/thread/"
        user = ForumUserFactory()
        token = generate_user_token(user)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description",
            "attachment": encoded_file
        }

        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        self.assertEqual(resp.json,
                         {"message": "Please make sure to include both attachment and attachment extension if you want "
                                     "to attach a file!"})

    def test_delete_thread_with_manager_user(self):
        create_url = "/thread/"
        delete_url = "/thread/delete/1/"

        forum_user = ForumUserFactory()
        manager_user = ManagerUserFactory()

        forum_user_token = generate_user_token(forum_user)
        manager_user_token = generate_user_token(manager_user)

        create_headers = {"Content-Type": "application/json", "Authorization": f"Bearer {forum_user_token}"}
        delete_headers = {"Content-Type": "application/json", "Authorization": f"Bearer {manager_user_token}"}

        data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description"
        }

        thread_resp = self.client.post(create_url, headers=create_headers, json=data)
        assert thread_resp.status_code == 201

        delete_resp = self.client.delete(delete_url, headers=delete_headers)

        self.assert200(delete_resp)
        self.assertEqual(delete_resp.json, {"message": "Thread deleted!"})

    def test_update_thread_without_being_creator(self):
        create_url = "/thread/"
        update_url = "/thread/update-data/1/"

        forum_user_one = ForumUserFactory()
        forum_user_two = ForumUserFactory()

        forum_user_one_token = generate_user_token(forum_user_one)
        forum_user_two_token = generate_user_token(forum_user_two)

        forum_user_one_headers = {"Content-Type": "application/json", "Authorization": f"Bearer {forum_user_one_token}"}
        forum_user_two_headers = {"Content-Type": "application/json", "Authorization": f"Bearer {forum_user_two_token}"}

        create_data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description"
        }

        update_data = {
            "title": "NEW TITLE!"
        }
        thread_resp = self.client.post(create_url, headers=forum_user_one_headers, json=create_data)
        assert thread_resp.status_code == 201

        update_resp = self.client.put(update_url, headers=forum_user_two_headers, json=update_data)
        self.assert401(update_resp)
        self.assertEqual(update_resp.json, {"message": "You are not the creator of the thread!"})

    def test_like_thread(self):
        create_url = "/thread/"
        like_url = "/thread/like/1/"

        user = ForumUserFactory()
        token = generate_user_token(user)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

        data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description"
        }

        thread = self.client.post(create_url, headers=headers, json=data)
        assert thread.status_code == 201

        like = self.client.put(like_url, headers=headers)
        self.assert200(like)

    def test_dislike_thread(self):
        create_url = "/thread/"
        like_url = "/thread/like/1/"
        dislike_url = "/thread/dislike/1/"

        user = ForumUserFactory()
        token = generate_user_token(user)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

        data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description"
        }

        thread = self.client.post(create_url, headers=headers, json=data)
        assert thread.status_code == 201

        like = self.client.put(like_url, headers=headers)
        assert like.status_code == 200

        dislike = self.client.put(dislike_url, headers=headers)
        assert dislike.status_code == 200

    def test_like_thread_when_liked_already(self):
        create_url = "/thread/"
        like_url = "/thread/like/1/"

        user = ForumUserFactory()
        token = generate_user_token(user)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

        data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description"
        }

        thread = self.client.post(create_url, headers=headers, json=data)
        assert thread.status_code == 201

        like = self.client.put(like_url, headers=headers)
        self.assert200(like)

        like_again = self.client.put(like_url, headers=headers)
        assert like_again.status_code == 406

    def test_like_thread_when_not_liked(self):
        create_url = "/thread/"
        dislike_url = "/thread/dislike/1/"

        user = ForumUserFactory()
        token = generate_user_token(user)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

        data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description"
        }
        thread = self.client.post(create_url, headers=headers, json=data)
        assert thread.status_code == 201

        dislike = self.client.put(dislike_url, headers=headers)
        assert dislike.status_code == 406

    def test_update_status(self):
        create_url = "/thread/"
        update_url = "/thread/manager/update-status/1/"

        user = ForumUserFactory()
        manager_user = ManagerUserFactory()

        user_token = generate_user_token(user)
        manager_token = generate_user_token(manager_user)
        user_headers = {"Content-Type": "application/json", "Authorization": f"Bearer {user_token}"}
        manager_headers = {"Content-Type": "application/json", "Authorization": f"Bearer {manager_token}"}

        data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description"
        }

        thread = self.client.post(create_url, headers=user_headers, json=data)
        assert thread.status_code == 201

        update_data = {
            "status": "closed"
        }

        update = self.client.put(update_url, headers=manager_headers, json=update_data)
        self.assert200(update)
        self.assertEqual(update.json, "Thread status was changed!")

    def test_update_status_same_status(self):
        create_url = "/thread/"
        update_url = "/thread/manager/update-status/1/"

        user = ForumUserFactory()
        manager_user = ManagerUserFactory()

        user_token = generate_user_token(user)
        manager_token = generate_user_token(manager_user)
        user_headers = {"Content-Type": "application/json", "Authorization": f"Bearer {user_token}"}
        manager_headers = {"Content-Type": "application/json", "Authorization": f"Bearer {manager_token}"}

        data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description"
        }

        thread = self.client.post(create_url, headers=user_headers, json=data)
        assert thread.status_code == 201

        update_data = {
            "status": "open"
        }

        update = self.client.put(update_url, headers=manager_headers, json=update_data)
        assert update.status_code == 406
        self.assertEqual(update.json, {"message": "Thread in this status already!"})

    def test_missing_thread_with_given_id(self):
        user = ForumUserFactory()
        token = generate_user_token(user)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

        for url, method in THREAD_ENDPOINTS:
            if url == "/thread/comment/1/" or url == "/thread/update-data/1/":
                data = {
                    "description": "Test description"
                }
                resp = eval(f"self.client.{method}('{url}', headers={headers}, json={data})")
            elif url == "/thread/delete/1/":
                user = ManagerUserFactory()
                token = generate_user_token(user)
                headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
                resp = eval(f"self.client.{method}('{url}', headers={headers})")
            else:
                resp = eval(f"self.client.{method}('{url}', headers={headers})")
            self.assert_404(resp)
            self.assertEqual(resp.json, {"message": "No thread found with this ID!"})






