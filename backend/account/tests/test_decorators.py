from django.http import JsonResponse, HttpRequest
from django.test import TestCase
from unittest.mock import MagicMock, patch

import account.decorators
import account.business as business


class RequiresLoginDecoratorTest(TestCase):
    def setUp(self):
        self.fake_request = HttpRequest()
        self.fake_request.COOKIES["auth_token"] = "fake_auth_token"

    def test_decorator_no_auth_token(self):
        def dummy_view(request, *args, **kwargs):
            return JsonResponse({}, status=200)

        decorated_view = account.decorators.requires_login()(dummy_view)

        response = decorated_view(HttpRequest())

        self.assertEqual(response.status_code, 401)

    @patch("account.business.validate_token")
    @patch("jamco.helper.read_request")
    def test_decorator_valid_auth_token(self, mock_read_request, mock_validate_token):
        mock_validate_token.return_value = MagicMock(id=1)
        mock_read_request.return_value = {"user_id": 1}

        def dummy_view(request, *args, **kwargs):
            return JsonResponse({}, status=200)

        decorated_view = account.decorators.requires_login()(dummy_view)

        response = decorated_view(self.fake_request)

        self.assertEqual(response.status_code, 200)

    @patch("account.business.validate_token")
    @patch("jamco.helper.read_request")
    def test_decorator_invalid_auth_token(self, mock_read_request, mock_validate_token):
        mock_validate_token.side_effect = Exception("Invalid token")
        mock_read_request.return_value = {"user_id": 1}

        def dummy_view(request, *args, **kwargs):
            return JsonResponse({}, status=200)

        decorated_view = account.decorators.requires_login()(dummy_view)

        response = decorated_view(self.fake_request)

        self.assertEqual(response.status_code, 401)

    @patch("account.business.validate_token")
    @patch("jamco.helper.read_request")
    def test_decorator_allow_friends(self, mock_read_request, mock_validate_token):
        user = MagicMock(id=1)
        friend = MagicMock(id=2)

        user.friends.filter.return_value.exists.return_value = True
        mock_validate_token.return_value = user
        mock_read_request.return_value = {"user_id": friend.id}

        def dummy_view(request, *args, **kwargs):
            return JsonResponse({}, status=200)

        decorated_view = account.decorators.requires_login(allow_friends=True)(dummy_view)

        response = decorated_view(self.fake_request)

        self.assertEqual(response.status_code, 200)

    @patch("account.business.validate_token")
    @patch("jamco.helper.read_request")
    def test_decorator_not_allow_friends(self, mock_read_request, mock_validate_token):
        user = MagicMock(id=1)
        friend = MagicMock(id=2)

        user.friends.filter.return_value.exists.return_value = False
        mock_validate_token.return_value = user
        mock_read_request.return_value = {"user_id": friend.id}

        def dummy_view(request, *args, **kwargs):
            return JsonResponse({}, status=200)

        decorated_view = account.decorators.requires_login(allow_friends=False)(dummy_view)

        response = decorated_view(self.fake_request)

        self.assertEqual(response.status_code, 401)
