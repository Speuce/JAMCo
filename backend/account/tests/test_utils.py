from django.test import TestCase
import json
from account.auth_utils import decrypt_token, encrypt_token
from datetime import datetime


class AuthUtilsTests(TestCase):
    def test_decrypt_token(self):
        token_fields = json.dumps({"google_id": "user_google_id", "last_login": "user_last_login"})
        encrypted_token = (
            "gAAAAABkAtpogyusnH4F6bM1CGlm2nOrxjlb"
            + "MUy6D8mGVoxmwE7hKyFGICegub5EyMGNX3d_"
            + "2kkbVPihnpBa2BOQHCa2msxL80bwUOt3ppiVo1"
            + "L4IowHe-AWyKDFu9yJloXTfucDYqBfFV3YSTw3-"
            + "laLH2ayNoD7Ph5LzGHlLWnw9ux4OH6Q_8M="
        )
        self.assertEqual(decrypt_token(encrypted_token), json.loads(token_fields))

    # This test only verifies token length, as content is unknown
    def test_encrypt_token(self):
        function_return = encrypt_token(
            "user_google_id", datetime.strptime("2023-03-03 01:28:02.710196+00:00", "%Y-%m-%d %H:%M:%S.%f%z")
        )
        self.assertEqual(len(function_return), 204)
