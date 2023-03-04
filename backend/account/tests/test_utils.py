from django.test import TestCase
import json
from account.auth_utils import decrypt_token, encrypt_token


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

    def test_encrypt_token(self):
        encrypted_token = (
            "gAAAAABkAtzF9zhTHv7JxXi0-bL3joXQraCxI5Tki9xEZ9acQB7QwW77sKiEi_4J5"
            + "DHm-y1CmrkpjFrOsAVQ0c3XukeSNMqU4n3jZqT7xQD-RhJ1nwyK8l58n-TFQYRY"
            + "ihVq0alWrg-NnZOhXsGdQ0FloJcbPxwa6P-vtTanuG_VX25oin3b60o="
        )
        self.assertEqual(encrypt_token("user_google_id", "user_last_login"), encrypted_token)
