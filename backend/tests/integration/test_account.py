import logging
import json
from django.test import TransactionTestCase
from django.urls import reverse
from django.http.cookie import SimpleCookie
from account.models import User, Privacy
from account.tests.factories import UserFactory, PrivacyFactory

logger = logging.getLogger(__name__)


class GetOrCreateAccountTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_create_account(self):
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "test", "client_id": "test"}),
            content_type="application/json",
            **self.header,
        )
        user_data = {
            "id": 1,
            "google_id": "1234567890",
            "username": 0,
            "image_url": "https://i.imgur.com/QJpNyuN.png",
            "last_name": "Doe",
            "birthday": None,
            "city": None,
            "country": None,
            "region": None,
            "email": "john.doe@gmail.com",
            "field_of_work": None,
            "first_name": "John",
            "friends": [],
            "received_friend_requests": [],
            "sent_friend_requests": [],
        }
        self.assertEqual(response.status_code, 200)
        # The query should return the User object. Since a mock is used,
        # the id is as given
        self.assertEqual(
            json.loads(response.content)["data"],
            user_data,
        )

        user_data["username"] = "0"
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(
            User.objects.get(google_id="1234567890").to_dict(),
            user_data,
        )

        # Verify User Privacy Created
        self.assertEqual(len(Privacy.objects.all()), 1)
        self.assertEqual(
            Privacy.objects.get(user__id=user_data["id"]).to_dict(),
            {"id": 1, "is_searchable": True, "share_kanban": True, "cover_letter_requestable": True},
        )


class UpdateAccountTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_update_account(self):
        # Create an account first
        user_resp = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "test", "client_id": "test"}),
            content_type="application/json",
            **self.header,
        )

        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(
            User.objects.get(google_id="1234567890").to_dict(),
            {
                "id": 1,
                "google_id": "1234567890",
                "username": "0",
                "image_url": "https://i.imgur.com/QJpNyuN.png",
                "last_name": "Doe",
                "birthday": None,
                "city": None,
                "country": None,
                "region": None,
                "email": "john.doe@gmail.com",
                "field_of_work": None,
                "first_name": "John",
                "friends": [],
                "received_friend_requests": [],
                "sent_friend_requests": [],
            },
        )

        # Try updating it, the request should succeed
        response = self.client.post(
            reverse("update_account"),
            json.dumps({"id": user_resp.json()["data"]["id"], "first_name": "Rob"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(
            User.objects.get(google_id="1234567890").to_dict(),
            {
                "id": 1,
                "google_id": "1234567890",
                "username": "0",
                "image_url": "https://i.imgur.com/QJpNyuN.png",
                "last_name": "Doe",
                "birthday": None,
                "city": None,
                "country": None,
                "region": None,
                "email": "john.doe@gmail.com",
                "field_of_work": None,
                "first_name": "Rob",
                "friends": [],
                "received_friend_requests": [],
                "sent_friend_requests": [],
            },
        )

    def test_invalid_account_update(self):
        # Create an account first
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "test", "client_id": "test"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(
            User.objects.get(google_id="1234567890").to_dict(),
            {
                "id": 1,
                "google_id": "1234567890",
                "username": "0",
                "image_url": "https://i.imgur.com/QJpNyuN.png",
                "email": "john.doe@gmail.com",
                "field_of_work": None,
                "first_name": "John",
                "last_name": "Doe",
                "birthday": None,
                "city": None,
                "country": None,
                "region": None,
                "friends": [],
                "received_friend_requests": [],
                "sent_friend_requests": [],
            },
        )

        # Should fail if the given fields don't exist
        response = self.client.post(
            reverse("update_account"),
            json.dumps({"google_id": "1234567890", "favourite_prof": "Rob"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(
            User.objects.get(google_id="1234567890").to_dict(),
            {
                "id": 1,
                "google_id": "1234567890",
                "username": "0",
                "image_url": "https://i.imgur.com/QJpNyuN.png",
                "last_name": "Doe",
                "birthday": None,
                "city": None,
                "country": None,
                "region": None,
                "email": "john.doe@gmail.com",
                "field_of_work": None,
                "first_name": "John",
                "friends": [],
                "received_friend_requests": [],
                "sent_friend_requests": [],
            },
        )


class CreatePrivacyTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_get_privacies(self):
        # Create an account first -- this generates privacies
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "test", "client_id": "test"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(User.objects.all()), 1)

        # Assert that the privacies exist as default
        user = json.loads(response.content)["data"]
        response = self.client.post(
            reverse("get_user_privacies"),
            json.dumps({"user_id": user["id"]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        privs = json.loads(response.content)
        self.assertEqual(
            privs, {"id": 1, "is_searchable": True, "share_kanban": True, "cover_letter_requestable": True}
        )

    def test_invalid_get_privacies(self):
        # Create an account first -- this generates privacies
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "test", "client_id": "test"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(len(Privacy.objects.all()), 1)

        # Assert that the privacies exist as default
        response = self.client.post(
            reverse("get_user_privacies"),
            json.dumps({"user_id": -1}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


class UpdatePrivacyTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_update_privacies(self):
        # Create an account first -- this generates privacies
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "test", "client_id": "test"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(User.objects.all()), 1)

        # Assert that the privacies exist as default
        user = json.loads(response.content)["data"]
        self.assertEqual(
            Privacy.objects.get(user__id=user["id"]).to_dict(),
            {"id": 1, "is_searchable": True, "share_kanban": True, "cover_letter_requestable": True},
        )

        newPriv = {"id": 1, "is_searchable": False, "share_kanban": True, "cover_letter_requestable": False}
        # Update privacies
        response = self.client.post(
            reverse("update_privacies"),
            json.dumps({"user_id": user["id"], "privacies": newPriv}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        outPriv = Privacy.objects.get(id=1).to_dict()
        self.assertEqual(newPriv, outPriv)

    def test_invalid_update_privacies(self):
        # Create an account first -- this generates privacies
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "test", "client_id": "test"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(User.objects.all()), 1)

        # Assert that the privacies exist as default
        user = json.loads(response.content)["data"]
        self.assertEqual(
            Privacy.objects.get(user__id=user["id"]).to_dict(),
            {"id": 1, "is_searchable": True, "share_kanban": True, "cover_letter_requestable": True},
        )

        newPriv = {"id": 1, "is_searchable": False, "share_kanban": True, "cover_letter_requestable": False}
        # Update privacies
        response = self.client.post(
            reverse("update_privacies"),
            json.dumps({"user_id": -1, "privacies": newPriv}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        outPriv = Privacy.objects.get(id=1).to_dict()
        self.assertNotEqual(newPriv, outPriv)


class SearchUsersByNameTest(TransactionTestCase):
    reset_sequences = True

    def test_search_from_multiple_users(self):
        user_one = UserFactory(first_name="Jojo", last_name="Jojo")
        PrivacyFactory(user=user_one)
        user_two = UserFactory(first_name="Bobby", last_name="Smith")
        PrivacyFactory(user=user_two)
        user_three = UserFactory(first_name="Bobby", last_name="Bill")
        PrivacyFactory(user=user_three, is_searchable=False)
        user_four = UserFactory(first_name="Joe", last_name="Joel")
        PrivacyFactory(user=user_four)
        user_five = UserFactory(first_name="Rob", last_name="Smith")
        PrivacyFactory(user=user_five)

        # Verify only the is_searchable Bobby is returned
        response = self.client.post(
            reverse("search_users_by_name"),
            json.dumps("Bobby"),
            content_type="application/json",
        )

        expected_results = [
            {"id": user_two.id, "first_name": user_two.first_name, "last_name": user_two.last_name, "country": None}
        ]
        user_list = json.loads(response.content)["user_list"]
        self.assertEqual(expected_results, user_list)

        # Search overlapping first/last names
        response = self.client.post(
            reverse("search_users_by_name"),
            json.dumps("Jo Jo"),
            content_type="application/json",
        )

        expected_results = [
            {"id": user_one.id, "first_name": user_one.first_name, "last_name": user_one.last_name, "country": None},
            {"id": user_four.id, "first_name": user_four.first_name, "last_name": user_four.last_name, "country": None},
        ]
        user_list = json.loads(response.content)["user_list"]
        self.assertEqual(expected_results, user_list)

        # Search on single token
        response = self.client.post(
            reverse("search_users_by_name"),
            json.dumps("Smith"),
            content_type="application/json",
        )

        expected_results = [
            {"id": user_two.id, "first_name": user_two.first_name, "last_name": user_two.last_name, "country": None},
            {"id": user_five.id, "first_name": user_five.first_name, "last_name": user_five.last_name, "country": None},
        ]
        user_list = json.loads(response.content)["user_list"]
        self.assertEqual(expected_results, user_list)

    def test_search_empty_whitespace(self):
        user_one = UserFactory(first_name="Jojo", last_name="Jojo")
        PrivacyFactory(user=user_one)

        # Search Empty String
        response = self.client.post(
            reverse("search_users_by_name"),
            json.dumps(""),
            content_type="application/json",
        )

        user_list = json.loads(response.content)["user_list"]
        self.assertEqual(len(user_list), 0)

        # Search Whitespace String
        response = self.client.post(
            reverse("search_users_by_name"),
            json.dumps("    "),
            content_type="application/json",
        )

        user_list = json.loads(response.content)["user_list"]
        self.assertEqual(len(user_list), 0)


class AccountTestCase(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_invalid_oauth_properties(self):
        # Try to create a user when providing an incorrect id
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "garbage", "client_id": "unusable"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(len(Privacy.objects.all()), 0)

        # No CSRF in Cookie
        self.client.cookies = SimpleCookie({"not_a_csrftoken": "not_the_droid"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }
        # Post the request
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "test", "client_id": "test"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(len(Privacy.objects.all()), 0)

        # No CSRF in Header
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "NOT_HTTP_X-CSRFToken": "actual_trash",
        }
        # Post the request
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "test", "client_id": "test"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(len(Privacy.objects.all()), 0)

        # CSRFs do not match
        self.client.cookies = SimpleCookie({"csrftoken": "one_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "other_csrf_token",
        }
        # Post the request
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "test", "client_id": "test"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(len(Privacy.objects.all()), 0)
