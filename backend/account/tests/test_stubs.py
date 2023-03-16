from account.stubs import stub_verify_oauth2_token
from django.test import TestCase


class OauthStubTests(TestCase):
    def test_stub_function_return(self):
        response = stub_verify_oauth2_token("test", "test")
        self.assertEqual(
            response,
            {
                "sub": "1234567890",
                "email": "john.doe@gmail.com",
                "picture": "https://i.imgur.com/QJpNyuN.png",
                "given_name": "John",
                "family_name": "Doe",
            },
        )

    def test_stub_function_error(self):
        with self.assertRaises(ValueError):
            stub_verify_oauth2_token("not_test", "not_test")
