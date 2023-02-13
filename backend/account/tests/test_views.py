from django.test import RequestFactory, TestCase
from django.http import JsonResponse
from .views import get_or_create_account


class GetOrCreateAccountTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_or_create_account(self):
        request = self.factory.post(
            "/get_or_create_account",
            data='{"credential": "test_credential", "client_id": test_id}',
            content_type="application/json",
        )
        response = get_or_create_account(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"data": "account_created"}')
        self.assertIsInstance(response, JsonResponse)
