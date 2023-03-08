import json
from django.test import TestCase
from django.urls import reverse
from column import query, business
from column.tests.factories import KanbanColumnFactory
from column.models import KanbanColumn
from account.tests.factories import UserFactory
from unittest.mock import patch


@patch("column.business.get_columns")
class GetColumnsTests(TestCase):
    def test_get_columns(self, mock_get_columns):
        user = UserFactory()
        # Make several columns
        KanbanColumnFactory(user=user, name="New column", column_number=0)
        KanbanColumnFactory(user=user, name="Newer column", column_number=1)
        KanbanColumnFactory(user=user, name="Even newer column", column_number=2)

        mock_get_columns.return_value = KanbanColumn.objects.all()

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

    def test_get_columns_error(self, mock_get_columns):
        mock_get_columns.side_effect = Exception("Error")
        response = self.client.post(
            reverse("get_columns"),
            json.dumps({"user_id": 999}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)


@patch("column.business.update_columns")
@patch("column.business.get_columns")
class UpdateColumnsTests(TestCase):
    def test_create_column(self, mock_get_columns, mock_update_columns):
        user = UserFactory()

        KanbanColumnFactory(user=user, name="New column", column_number=0)

        mock_update_columns.return_value = KanbanColumn.objects.all()

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
        KanbanColumnFactory(user=user, name="Newer column", column_number=1)

        mock_update_columns.return_value = KanbanColumn.objects.all()
        mock_get_columns.return_value = KanbanColumn.objects.all()

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

    def test_invalid_request(self, mock_get_columns, mock_update_columns):
        user = UserFactory()
        col = KanbanColumnFactory(user=user)
        mock_update_columns.side_effect = Exception("Error")
        mock_get_columns.return_value = KanbanColumn.objects.all()

        # User doesn't exist
        response = self.client.post(
            reverse("update_columns"),
            json.dumps(
                {
                    "user_id": -1,
                    "payload": [{"id": col.id, "name": "THE column", "column_number": 0}],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        # Make sure the request didn't update anything
        self.assertEqual(business.get_columns(user.id)[0].name, "Column Name")

    def test_rename(self, mock_get_columns, mock_update_columns):
        user = UserFactory()
        col1 = KanbanColumnFactory(user=user, name="Old column", column_number=0)
        col2 = KanbanColumnFactory(user=user, name="The most powerful column", column_number=1)
        col3 = KanbanColumnFactory(user=user, name="Even newer column", column_number=2)

        mock_update_columns.return_value = KanbanColumn.objects.all()
        mock_get_columns.return_value = KanbanColumn.objects.all()

        # Rename a couple of them
        response = self.client.post(
            reverse("update_columns"),
            json.dumps(
                {
                    "user_id": user.id,
                    "payload": [
                        {"id": col1.id, "name": "Old column", "column_number": 0},
                        {
                            "id": col2.id,
                            "name": "The most powerful column",
                            "column_number": 1,
                        },
                        {
                            "id": col3.id,
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

    def test_reorder(self, mock_get_columns, mock_update_columns):
        user = UserFactory()
        col1 = KanbanColumnFactory(user=user, name="New column", column_number=1)
        col2 = KanbanColumnFactory(user=user, name="Newer column", column_number=2)
        col3 = KanbanColumnFactory(user=user, name="Even newer column", column_number=0)

        mock_update_columns.return_value = KanbanColumn.objects.all().order_by("column_number")
        mock_get_columns.return_value = KanbanColumn.objects.all()

        # Make the third one be the first
        response = self.client.post(
            reverse("update_columns"),
            json.dumps(
                {
                    "user_id": user.id,
                    "payload": [
                        {"id": col1.id, "name": "New column", "column_number": 1},
                        {
                            "id": col2.id,
                            "name": "Newer column",
                            "column_number": 2,
                        },
                        {
                            "id": col3.id,
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
        self.assertEqual(response_columns[0]["id"], col3.id)
        self.assertEqual(response_columns[1]["id"], col1.id)
        self.assertEqual(response_columns[2]["id"], col2.id)
        self.assertEqual(len(query.get_columns(user.id)), 3)

    def test_out_of_bounds_reorder(self, mock_get_columns, mock_update_columns):
        user = UserFactory()
        col3 = KanbanColumnFactory(user=user, name="Even newer column", column_number=0)
        col1 = KanbanColumnFactory(user=user, name="New column", column_number=1)
        col2 = KanbanColumnFactory(user=user, name="Newer column", column_number=2)

        mock_get_columns.return_value = KanbanColumn.objects.all()
        mock_update_columns.return_value = KanbanColumn.objects.all()

        # Make the third one be the first. Er, the one at index negative-fifty.
        # It should be treated as index zero anyway.
        response = self.client.post(
            reverse("update_columns"),
            json.dumps(
                {
                    "user_id": user.id,
                    "payload": [
                        {"id": col1.id, "name": "New column", "column_number": 0},
                        {
                            "id": col2.id,
                            "name": "Newer column",
                            "column_number": 1,
                        },
                        {
                            "id": col3.id,
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
        self.assertEqual(response_columns[0]["id"], col3.id)
        self.assertEqual(response_columns[1]["id"], col1.id)
        self.assertEqual(response_columns[2]["id"], col2.id)
        self.assertEqual(len(query.get_columns(user.id)), 3)

        KanbanColumn.objects.all().delete()
        col1 = KanbanColumnFactory(user=user, name="New column", column_number=0)
        col2 = KanbanColumnFactory(user=user, name="Newer column", column_number=1)
        col3 = KanbanColumnFactory(user=user, name="Even newer column", column_number=2)

        mock_get_columns.return_value = KanbanColumn.objects.all()
        mock_update_columns.return_value = KanbanColumn.objects.all()

        # Do the same but with the index being invalid in the other direction
        response = self.client.post(
            reverse("update_columns"),
            json.dumps(
                {
                    "user_id": user.id,
                    "payload": [
                        {
                            "id": col3.id,
                            "name": "Even newer column",
                            "column_number": 500,
                        },
                        {"id": col1.id, "name": "New column", "column_number": 0},
                        {
                            "id": col2.id,
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
        self.assertEqual(response_columns[0]["id"], col1.id)
        self.assertEqual(response_columns[1]["id"], col2.id)
        self.assertEqual(response_columns[2]["id"], col3.id)
        self.assertEqual(len(query.get_columns(user.id)), 3)

    def test_delete(self, mock_get_columns, mock_update_columns):
        user = UserFactory()
        col1 = KanbanColumnFactory(user=user, name="New column", column_number=1)
        col3 = KanbanColumnFactory(user=user, name="Even newer column", column_number=0)

        mock_update_columns.return_value = KanbanColumn.objects.all()
        mock_get_columns.return_value = KanbanColumn.objects.all()

        response = self.client.post(
            reverse("update_columns"),
            json.dumps(
                {
                    "user_id": user.id,
                    "payload": [
                        {
                            "id": col3.id,
                            "name": "Even newer column",
                            "column_number": 2,
                        },
                        {"id": col1.id, "name": "New column", "column_number": 0},
                    ],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_columns = json.loads(response.content)["columns"]
        # Since column 1 was absent from the update request, it should be gone
        self.assertEqual(response_columns[0]["id"], col1.id)
        self.assertEqual(response_columns[1]["id"], col3.id)
        self.assertEqual(len(query.get_columns(user.id)), 2)

    def test_nonexistent_user(self, mock_get_columns, mock_update_columns):
        mock_update_columns.side_effect = Exception("User doesnt exist")
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
        self.assertEqual(
            json.loads(response.content),
            {"error": "Exception('User doesnt exist')"},
        )

    def test_empty_payload(self, mock_get_columns, mock_update_columns):
        user = UserFactory()
        KanbanColumn(user=user)

        mock_update_columns.return_value = KanbanColumn.objects.all()
        mock_get_columns.return_value = KanbanColumn.objects.all()

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
