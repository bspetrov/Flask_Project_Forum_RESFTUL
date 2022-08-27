from unittest.mock import patch

from flask_testing import TestCase

from config import create_app
from db import db
from services.ses import SimpleEmailService
from tests.factories import ForumUserFactory
from tests.helpers import generate_user_token

LOGIN_REQUIRED_ENDPOINTS = (
    ("/thread/get/1/", "GET"),
    ("/thread/", "POST"),
    ("/thread/comment/1/", "POST"),
    ("/thread/like/1/", "PUT"),
    ("/thread/dislike/1/", "PUT"),
    ("/thread/update-data/1/", "PUT"),
)

PERMISSION_REQUIRED_ENDPOINTS = (
    ("/thread/delete/1/", "DELETE"),
    ("/thread/manager/update-status/1/", "PUT")

)


class TestApp(TestCase):
    def create_app(self):
        return create_app("config.TestConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def iterate_endpoints(
            self,
            endpoints_data,
            status_code_method,
            expected_resp_body,
            headers=None,
            payload=None,
    ):
        if not headers:
            headers = {}
        if not payload:
            payload = {}

        resp = None
        for url, method in endpoints_data:
            if method == "GET":
                resp = self.client.get(url, headers=headers)
            elif method == "POST":
                resp = self.client.post(url, headers=headers)
            elif method == "PUT":
                resp = self.client.put(url, headers=headers)
            elif method == "DELETE":
                resp = self.client.delete(url, headers=headers)
            status_code_method(resp)
            self.assertEqual(resp.json, expected_resp_body)

    @patch.object(SimpleEmailService, "send_mail", return_value="Mail sent")
    def test_register_email_send(self, ses_mock):
        url = "/register/"

        data = {
            "username": "Test",
            "password": "Test123123123",
            "first_name": "Testing",
            "last_name": "Testov",
            "email": "email@email.com"
        }

        headers = {"Content-Type": "application/json"}

        resp = self.client.post(url, headers=headers, json=data)
        assert resp.status_code == 201

    def test_login_required(self):
        self.iterate_endpoints(LOGIN_REQUIRED_ENDPOINTS, self.assert_401, {"message": "Missing token!"})

    def test_invalid_token(self):
        headers = {
            "Authorization": "Bearer asdzxfAasdzx123"
        }

        self.iterate_endpoints(LOGIN_REQUIRED_ENDPOINTS, self.assert_401, {"message": "Invalid token"}, headers)

    def test_expired_token(self):
        pass

    def test_missing_manager_permissions(self):
        user = ForumUserFactory()
        token = generate_user_token(user)
        headers = {"Authorization": f"Bearer {token}"}
        resp = None

        for url, method in PERMISSION_REQUIRED_ENDPOINTS:
            if method == "PUT":
                resp = self.client.put(url, headers=headers)
            if method == "DELETE":
                resp = self.client.delete(url, headers=headers)

            self.assert_403(resp)
            self.assertEqual(resp.json, {"message": "Permission denied!"})
