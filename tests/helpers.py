from managers.auth import AuthManager


def generate_user_token(user):
    token = AuthManager.encode_token(user)
    return token


def mock_uuid():
    return "1111-1111-1111-1111"


encoded_file = "VGhpcyBpcyBhIHRlc3QgZmlsZQ=="
encoded_file_extension = "txt"
