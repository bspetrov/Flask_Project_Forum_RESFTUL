from flask_testing import TestCase

from config import create_app
from db import db
from tests.factories import ForumUserFactory
from tests.helpers import generate_user_token


class TestComment(TestCase):

    def create_app(self):
        return create_app("config.TestConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_crate_single_comment(self):
        thread_url = "/thread/"
        get_url = "/comment/get/1/"
        create_url = "/thread/comment/1/"

        user = ForumUserFactory()
        token = generate_user_token(user)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

        comment_data = {
            "description": "Checking out and entering another comment!"
        }

        thread_data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description",
        }

        create_thread = self.client.post(thread_url, headers=headers, json=thread_data)
        assert create_thread.status_code == 201

        create_comment = self.client.post(create_url, headers=headers, json=comment_data)
        self.assert200(create_comment)

        get_resp = self.client.get(get_url, headers=headers)
        self.assert200(get_resp)

    def test_edit_single_comment(self):
        thread_url = "/thread/"
        create_url = "/thread/comment/1/"
        edit_url = "/comment/edit/1/"

        user = ForumUserFactory()
        token = generate_user_token(user)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

        thread_data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description",
        }

        create_thread = self.client.post(thread_url, headers=headers, json=thread_data)
        assert create_thread.status_code == 201

        comment_data = {
            "description": "Checking out and entering another comment!"
        }

        create_resp = self.client.post(create_url, headers=headers, json=comment_data)
        self.assert200(create_resp)

        new_comment_data = {
            "description": "TEST!"
        }

        edit_resp = self.client.put(edit_url, headers=headers, json=new_comment_data)
        self.assert200(edit_resp)

    def test_like_single_comment(self):
        thread_url = "/thread/"
        create_url = "/thread/comment/1/"
        like_url = "/comment/like/1/"

        user = ForumUserFactory()
        token = generate_user_token(user)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

        thread_data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description",
        }

        create_thread = self.client.post(thread_url, headers=headers, json=thread_data)
        assert create_thread.status_code == 201

        comment_data = {
            "description": "Checking out and entering another comment!"
        }

        create_resp = self.client.post(create_url, headers=headers, json=comment_data)
        self.assert200(create_resp)

        like_resp = self.client.put(like_url, headers=headers)
        self.assert200(like_resp)

    def test_dislike_single_comment(self):
        thread_url = "/thread/"
        create_url = "/thread/comment/1/"
        like_url = "/comment/like/1/"
        dislike_url = "/comment/dislike/1/"

        user = ForumUserFactory()
        token = generate_user_token(user)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

        thread_data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description",
        }

        create_thread = self.client.post(thread_url, headers=headers, json=thread_data)
        assert create_thread.status_code == 201

        comment_data = {
            "description": "Checking out and entering another comment!"
        }

        create_resp = self.client.post(create_url, headers=headers, json=comment_data)
        self.assert200(create_resp)

        like_resp = self.client.put(like_url, headers=headers)
        self.assert200(like_resp)

        dislike_resp = self.client.put(dislike_url, headers=headers)
        self.assert200(dislike_resp)

    def test_like_if_liked(self):
        thread_url = "/thread/"
        create_url = "/thread/comment/1/"
        like_url = "/comment/like/1/"

        user = ForumUserFactory()
        token = generate_user_token(user)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

        thread_data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description",
        }

        create_thread = self.client.post(thread_url, headers=headers, json=thread_data)
        assert create_thread.status_code == 201

        comment_data = {
            "description": "Checking out and entering another comment!"
        }

        create_resp = self.client.post(create_url, headers=headers, json=comment_data)
        self.assert200(create_resp)

        like_resp = self.client.put(like_url, headers=headers)
        self.assert200(like_resp)

        like_again_resp = self.client.put(like_url, headers=headers)
        assert like_again_resp.status_code == 406

    def test_dislike_not_liked(self):
        thread_url = "/thread/"
        create_url = "/thread/comment/1/"
        dislike_url = "/comment/dislike/1/"

        user = ForumUserFactory()
        token = generate_user_token(user)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

        thread_data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description",
        }

        create_thread = self.client.post(thread_url, headers=headers, json=thread_data)
        assert create_thread.status_code == 201

        comment_data = {
            "description": "Checking out and entering another comment!"
        }

        create_resp = self.client.post(create_url, headers=headers, json=comment_data)
        self.assert200(create_resp)

        dislike_resp = self.client.put(dislike_url, headers=headers)
        assert dislike_resp.status_code == 406

    def test_delete_comment(self):
        thread_url = "/thread/"
        create_url = "/thread/comment/1/"
        delete_url = "/comment/delete/1/"

        user = ForumUserFactory()
        token = generate_user_token(user)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

        comment_data = {
            "description": "Checking out and entering another comment!"
        }

        thread_data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description",
        }

        create_thread = self.client.post(thread_url, headers=headers, json=thread_data)
        assert create_thread.status_code == 201

        create_comment = self.client.post(create_url, headers=headers, json=comment_data)
        self.assert200(create_comment)

        delete_comment = self.client.delete(delete_url, headers=headers)
        self.assert200(delete_comment)

    def test_delete_comment_but_diff_user(self):
        thread_url = "/thread/"
        create_url = "/thread/comment/1/"
        delete_url = "/comment/delete/1/"

        user = ForumUserFactory()
        user_two = ForumUserFactory()
        token = generate_user_token(user)
        token_two = generate_user_token(user_two)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        headers_two = {"Content-Type": "application/json", "Authorization": f"Bearer {token_two}"}


        comment_data = {
            "description": "Checking out and entering another comment!"
        }

        thread_data = {
            "title": "Test title",
            "category": "gaming",
            "description": "Test description",
        }

        create_thread = self.client.post(thread_url, headers=headers, json=thread_data)
        assert create_thread.status_code == 201

        create_comment = self.client.post(create_url, headers=headers, json=comment_data)
        self.assert200(create_comment)

        delete_comment = self.client.delete(delete_url, headers=headers_two)
        self.assert401(delete_comment)





