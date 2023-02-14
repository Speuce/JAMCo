import json
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from account import business, query
from unittest import mock
from django.http.cookie import SimpleCookie
from django.core.exceptions import ObjectDoesNotExist
from account import query, models


@mock.patch("google.oauth2.id_token.verify_oauth2_token")
class GetOrCreateAccountTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_create_account(self, mock_verify_oauth2_token):
        mock_verify_oauth2_token.return_value = {
            "sub": "unique_user_id",
            "given_name": "firstname",
            "email": "useremail",
        }
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "whatever", "client_id": "8675309"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 200)
        # The query should return the User object. Since a mock is used,
        # the id is as given
        self.assertEqual(
            json.loads(response.content)["data"],
            {
                "google_id": "unique_user_id",
                "username": 0,
                "image_url": None,
                "last_name": "",
                "birthday": None,
                "city": None,
                "country": None,
                "email": "useremail",
                "field_of_work": None,
                "first_name": "firstname",
                "last_login": None,
            },
        )


@mock.patch("google.oauth2.id_token.verify_oauth2_token")
class UpdateAccountTests(TestCase):
    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_update_account(self, mock_verify_oauth2_token):
        mock_verify_oauth2_token.return_value = {
            "sub": "unique_user_id",
            "given_name": "firstname",
            "email": "useremail",
        }
        # Create an account first
        self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "whatever", "client_id": "8675309"}),
            content_type="application/json",
            **self.header,
        )

        # Try updating it, the request should succeed
        response = self.client.post(
            reverse("update_account"),
            json.dumps({"google_id": "unique_user_id", "first_name": "Rob"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_account_update(self, mock_verify_oauth2_token):
        mock_verify_oauth2_token.return_value = {
            "sub": "unique_user_id",
            "given_name": "firstname",
            "email": "useremail",
        }
        # Create an account first
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "unique_user_id", "client_id": "8675309"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 200)

        # Should fail if the given fields don't exist
        response = self.client.post(
            reverse("update_account"),
            json.dumps({"google_id": "unique_user_id", "favourite_prof": "Rob"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


class GetColumnsTests(TestCase):
    def test_get_columns(self):
        user = query.get_or_create_user({"sub": "4"})
        # Make several columns
        query.create_column(user.id, "New column", 0)
        query.create_column(user.id, "Newer column", 1)
        query.create_column(user.id, "Even newer column", 2)

        response = self.client.post(
            reverse("get_columns"),
            json.dumps({"user_id": user.id}),
            content_type="application/json",
        )

        response_columns = json.loads(response.content)["columns"]
        self.assertEqual(response_columns[0]["name"], "New column")
        self.assertEqual(response_columns[0]["column_number"], 0)
        self.assertEqual(response_columns[1]["name"], "Newer column")
        self.assertEqual(response_columns[1]["column_number"], 1)
        self.assertEqual(response_columns[2]["name"], "Even newer column")
        self.assertEqual(response_columns[2]["column_number"], 2)
        self.assertEqual(len(query.get_columns(user.id)), 3)

        self.assertEqual(response.status_code, 200)


class UpdateColumnsTests(TestCase):
    def test_create_column(self):
        user = query.get_or_create_user({"sub": "4"})

        response = self.client.post(
            reverse("update_columns"),
            json.dumps(
                {
                    "user_id": user.id,
                    "payload": [{"id": -1, "name": "New column", "column_number": 0}],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        columns = json.loads(response.content)["columns"]

        self.assertEqual(columns[0]["name"], "New column")
        self.assertEqual(columns[0]["column_number"], 0)

        # Make a second column and make sure the first one is still there
        response = self.client.post(
            reverse("update_columns"),
            json.dumps(
                {
                    "user_id": user.id,
                    "payload": [
                        {
                            "id": columns[0]["id"],
                            "name": "New column",
                            "column_number": 0,
                        },
                        {"id": -1, "name": "Newer column", "column_number": 1},
                    ],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        columns = json.loads(response.content)["columns"]

        self.assertEqual(columns[0]["name"], "New column")
        self.assertEqual(columns[0]["column_number"], 0)
        self.assertEqual(columns[1]["name"], "Newer column")
        self.assertEqual(columns[1]["column_number"], 1)
        self.assertEqual(len(query.get_columns(user.id)), 2)

    def test_invalid_request(self):
        user = query.get_or_create_user({"sub": "4"})
        columns = business.update_columns(
            user.id,
            [
                {"id": -1, "name": "New column", "column_number": 0},
                {"id": -1, "name": "Newer column", "column_number": 1},
                {"id": -1, "name": "Even newer column", "column_number": 2},
            ],
        )

        # User doesn't exist
        response = self.client.post(
            reverse("update_columns"),
            json.dumps(
                {
                    "user_id": -1,
                    "payload": [
                        {"id": columns[0].id, "name": "THE column", "column_number": 0}
                    ],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        # Make sure the request didn't update anything
        self.assertEqual(business.get_columns(user.id)[0].name, "New column")

    def test_rename(self):
        user = query.get_or_create_user({"sub": "4"})
        columns = business.update_columns(
            user.id,
            [
                {"id": -1, "name": "New column", "column_number": 0},
                {"id": -1, "name": "Newer column", "column_number": 1},
                {"id": -1, "name": "Even newer column", "column_number": 2},
            ],
        )

        # Rename a couple of them
        response = self.client.post(
            reverse("update_columns"),
            json.dumps(
                {
                    "user_id": user.id,
                    "payload": [
                        {"id": columns[0].id, "name": "Old column", "column_number": 0},
                        {
                            "id": columns[1].id,
                            "name": "The most powerful column",
                            "column_number": 1,
                        },
                        {
                            "id": columns[2].id,
                            "name": "Even newer column",
                            "column_number": 2,
                        },
                    ],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        columns = json.loads(response.content)["columns"]
        self.assertEqual(columns[0]["name"], "Old column")
        self.assertEqual(columns[0]["column_number"], 0)
        self.assertEqual(columns[1]["name"], "The most powerful column")
        self.assertEqual(columns[1]["column_number"], 1)
        self.assertEqual(columns[2]["name"], "Even newer column")
        self.assertEqual(columns[2]["column_number"], 2)
        self.assertEqual(len(query.get_columns(user.id)), 3)

    def test_reorder(self):
        user = query.get_or_create_user({"sub": "4"})
        columns = business.update_columns(
            user.id,
            [
                {"id": -1, "name": "New column", "column_number": 0},
                {"id": -1, "name": "Newer column", "column_number": 1},
                {"id": -1, "name": "Even newer column", "column_number": 2},
            ],
        )

        # Make the third one be the first
        response = self.client.post(
            reverse("update_columns"),
            json.dumps(
                {
                    "user_id": user.id,
                    "payload": [
                        {"id": columns[0].id, "name": "New column", "column_number": 1},
                        {
                            "id": columns[1].id,
                            "name": "Newer column",
                            "column_number": 2,
                        },
                        {
                            "id": columns[2].id,
                            "name": "Even newer column",
                            "column_number": 0,
                        },
                    ],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_columns = json.loads(response.content)["columns"]
        self.assertEqual(response_columns[0]["id"], columns[2].id)
        self.assertEqual(response_columns[1]["id"], columns[0].id)
        self.assertEqual(response_columns[2]["id"], columns[1].id)
        self.assertEqual(len(query.get_columns(user.id)), 3)

    def test_out_of_bounds_reorder(self):
        user = query.get_or_create_user({"sub": "4"})
        columns = business.update_columns(
            user.id,
            [
                {"id": -1, "name": "New column", "column_number": 0},
                {"id": -1, "name": "Newer column", "column_number": 1},
                {"id": -1, "name": "Even newer column", "column_number": 2},
            ],
        )

        # Make the third one be the first. Er, the one at index negative-fifty.
        # It should be treated as index zero anyway.
        response = self.client.post(
            reverse("update_columns"),
            json.dumps(
                {
                    "user_id": user.id,
                    "payload": [
                        {"id": columns[0].id, "name": "New column", "column_number": 0},
                        {
                            "id": columns[1].id,
                            "name": "Newer column",
                            "column_number": 1,
                        },
                        {
                            "id": columns[2].id,
                            "name": "Even newer column",
                            "column_number": -50,
                        },
                    ],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_columns = json.loads(response.content)["columns"]
        self.assertEqual(response_columns[0]["id"], columns[2].id)
        self.assertEqual(response_columns[1]["id"], columns[0].id)
        self.assertEqual(response_columns[2]["id"], columns[1].id)
        self.assertEqual(len(query.get_columns(user.id)), 3)

        # Do the same but with the index being invalid in the other direction
        response = self.client.post(
            reverse("update_columns"),
            json.dumps(
                {
                    "user_id": user.id,
                    "payload": [
                        {
                            "id": columns[2].id,
                            "name": "Even newer column",
                            "column_number": 500,
                        },
                        {"id": columns[0].id, "name": "New column", "column_number": 0},
                        {
                            "id": columns[1].id,
                            "name": "Newer column",
                            "column_number": 1,
                        },
                    ],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_columns = json.loads(response.content)["columns"]
        self.assertEqual(response_columns[0]["id"], columns[0].id)
        self.assertEqual(response_columns[1]["id"], columns[1].id)
        self.assertEqual(response_columns[2]["id"], columns[2].id)
        self.assertEqual(len(query.get_columns(user.id)), 3)

    def test_delete(self):
        user = query.get_or_create_user({"sub": "4"})
        columns = business.update_columns(
            user.id,
            [
                {"id": -1, "name": "New column", "column_number": 0},
                {"id": -1, "name": "Newer column", "column_number": 1},
                {"id": -1, "name": "Even newer column", "column_number": 2},
            ],
        )

        response = self.client.post(
            reverse("update_columns"),
            json.dumps(
                {
                    "user_id": user.id,
                    "payload": [
                        {
                            "id": columns[2].id,
                            "name": "Even newer column",
                            "column_number": 2,
                        },
                        {"id": columns[0].id, "name": "New column", "column_number": 0},
                    ],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_columns = json.loads(response.content)["columns"]
        # Since column 1 was absent from the update request, it should be gone
        self.assertEqual(response_columns[0]["id"], columns[0].id)
        self.assertEqual(response_columns[1]["id"], columns[2].id)
        self.assertEqual(len(query.get_columns(user.id)), 2)

    def test_nonexistent_user(self):
        response = self.client.post(
            reverse("update_columns"),
            json.dumps(
                {
                    "user_id": -1,
                    "payload": [{"id": -1, "name": "Where am I", "column_number": 0}],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {})

    def test_empty_payload(self):
        user = query.get_or_create_user({"sub": "4"})
        business.update_columns(
            user.id,
            [
                {"id": -1, "name": "New column", "column_number": 0},
                {"id": -1, "name": "Newer column", "column_number": 1},
                {"id": -1, "name": "Even newer column", "column_number": 2},
            ],
        )

        # If the user has columns, an empty update should delete all of them
        response = self.client.post(
            reverse("update_columns"),
            json.dumps({"user_id": user.id, "payload": []}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_columns = json.loads(response.content)["columns"]
        self.assertEqual(len(response_columns), 0)
        self.assertEqual(len(query.get_columns(user.id)), 0)

        # After that, an empty update shouldn't do anything
        response = self.client.post(
            reverse("update_columns"),
            json.dumps({"user_id": user.id, "payload": []}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_columns = json.loads(response.content)["columns"]
        self.assertEqual(len(response_columns), 0)
        self.assertEqual(len(query.get_columns(user.id)), 0)


@mock.patch("google.oauth2.id_token.verify_oauth2_token")
class AccountTestCase(TestCase):
    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_invalid_oauth_properties(self, mock_verify_oauth2_token):
        # Try to create a user when providing an incorrect id
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "garbage", "client_id": "unusable"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)

        ## No CSRF in Cookie
        self.client.cookies = SimpleCookie({"not_a_csrftoken": "not_the_droid"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }
        # Post the request
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "whatever", "client_id": "8675309"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)

        ## No CSRF in Header
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "NOT_HTTP_X-CSRFToken": "actual_trash",
        }
        # Post the request
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "whatever", "client_id": "8675309"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)

        ## CSRFs do not match
        self.client.cookies = SimpleCookie({"csrftoken": "one_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "other_csrf_token",
        }
        # Post the request
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "whatever", "client_id": "8675309"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)
