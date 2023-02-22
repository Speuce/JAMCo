from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from column import query, business
from account.tests.factories import UserFactory
from column.tests.factories import KanbanColumnFactory
from column.models import KanbanColumn
from unittest.mock import patch


class CreateDefaultColumnsTests(TestCase):
    @patch("column.query.create_column")
    def test_default_columns(self, mock_create_column):
        user = UserFactory()
        business.create_default_columns(user.id)
        mock_create_column.assert_any_call(user.id, "To Apply", 0)
        mock_create_column.assert_any_call(user.id, "Application Submitted", 1)
        mock_create_column.assert_any_call(user.id, "OA", 2)
        mock_create_column.assert_any_call(user.id, "Interview", 3)
        self.assertEqual(mock_create_column.call_count, 4)


class GetColumnsTests(TestCase):
    @patch("column.query.get_columns")
    def test_get_columns(self, mock_get_columns):
        user = UserFactory()
        KanbanColumnFactory(user=user, column_number=0)
        KanbanColumnFactory(user=user, column_number=1)
        KanbanColumnFactory(user=user, column_number=2)

        mock_get_columns.return_value = KanbanColumn.objects.all()

        columns = business.get_columns(user.id)
        column_numbers = [column.column_number for column in columns]
        # Returned columns should be sorted by column number
        self.assertTrue(all(column_numbers[i] <= column_numbers[i + 1] for i in range(len(column_numbers) - 1)))


@patch("column.query.get_columns")
@patch("column.query.delete_columns")
@patch("column.query.create_column")
class UpdateColumnsTests(TestCase):
    def test_rename(self, mock_create_column, mock_delete_column, mock_get_columns):
        user = UserFactory()
        col1 = KanbanColumnFactory(user=user, column_number=0, name="Old column")
        col2 = KanbanColumnFactory(user=user, column_number=1)
        col3 = KanbanColumnFactory(user=user, column_number=2)

        all_mocks = KanbanColumn.objects.all()
        all_mocks[1].name = "The most powerful column"
        all_mocks[2].name = "Even newer column"
        mock_get_columns.return_value = all_mocks

        # Rename the first two
        columns = business.update_columns(
            user.id,
            [
                {"id": col1.id, "name": "Old column", "column_number": 0},
                {
                    "id": col2.id,
                    "name": "The most powerful column",
                    "column_number": 1,
                },
                {"id": col3.id, "name": "Even newer column", "column_number": 2},
            ],
        )

        self.assertEqual(columns[0].name, "Old column")
        self.assertEqual(columns[0].column_number, 0)
        self.assertEqual(columns[1].name, "The most powerful column")
        self.assertEqual(columns[1].column_number, 1)
        self.assertEqual(columns[2].name, "Even newer column")
        self.assertEqual(columns[2].column_number, 2)
        self.assertEqual(len(query.get_columns(user.id)), 3)

    def test_reorder(self, mock_create_column, mock_delete_column, mock_get_columns):
        user = UserFactory()
        col1 = KanbanColumnFactory(user=user, column_number=0)
        col2 = KanbanColumnFactory(user=user, column_number=1)
        col3 = KanbanColumnFactory(user=user, column_number=2)

        all_mocks = KanbanColumn.objects.all()
        all_mocks[2].column_number = 0
        all_mocks[0].column_number = 3
        mock_get_columns.return_value = all_mocks

        # Make the third one be the first
        result_columns = business.update_columns(
            user.id,
            [
                {"id": col1.id, "name": "New column", "column_number": 1},
                {"id": col2.id, "name": "Newer column", "column_number": 2},
                {"id": col3.id, "name": "Even newer column", "column_number": 0},
            ],
        )

        self.assertEqual(result_columns[0].id, col3.id)
        self.assertEqual(result_columns[1].id, col1.id)
        self.assertEqual(result_columns[2].id, col2.id)
        self.assertEqual(len(query.get_columns(user.id)), 3)

    def test_out_of_bounds_reorder(self, mock_create_column, mock_delete_column, mock_get_columns):
        user = UserFactory()
        col1 = KanbanColumnFactory(user=user, column_number=0)
        col2 = KanbanColumnFactory(user=user, column_number=1)
        col3 = KanbanColumnFactory(user=user, column_number=2)

        all_mocks = KanbanColumn.objects.all()
        all_mocks[2].column_number = 0
        mock_get_columns.return_value = all_mocks

        # Make the third one be the first. Er, the one at index negative-fifty.
        # It should be treated as index zero anyway.
        result_columns = business.update_columns(
            user.id,
            [
                {"id": col1.id, "name": "New column", "column_number": 1},
                {"id": col2.id, "name": "Newer column", "column_number": 2},
                {
                    "id": col3.id,
                    "name": "Even newer column",
                    "column_number": -50,
                },
            ],
        )

        self.assertEqual(result_columns[0].id, col3.id)
        self.assertEqual(result_columns[1].id, col1.id)
        self.assertEqual(result_columns[2].id, col2.id)
        self.assertEqual(len(query.get_columns(user.id)), 3)

        all_mocks = KanbanColumn.objects.all()
        all_mocks[2].column_number = 2
        mock_get_columns.return_value = all_mocks

        # Do the same but with the index being invalid in the other direction
        result_columns = business.update_columns(
            user.id,
            [
                {
                    "id": col1.id,
                    "name": "Even newer column",
                    "column_number": 500,
                },
                {"id": col2.id, "name": "New column", "column_number": 0},
                {"id": col3.id, "name": "Newer column", "column_number": 1},
            ],
        )

        self.assertEqual(result_columns[0].id, col2.id)
        self.assertEqual(result_columns[1].id, col3.id)
        self.assertEqual(result_columns[2].id, col1.id)
        self.assertEqual(len(query.get_columns(user.id)), 3)

    def test_delete(self, mock_create_column, mock_delete_column, mock_get_columns):
        user = UserFactory()
        col1 = KanbanColumnFactory(user=user, column_number=0)
        col2 = KanbanColumnFactory(user=user, column_number=1)
        col3 = KanbanColumnFactory(user=user, column_number=2)

        all = KanbanColumn.objects.all()
        all.filter(id=col2.id).delete()
        mock_get_columns.return_value = all

        result_columns = business.update_columns(
            user.id,
            [
                {"id": col3.id, "name": "Even newer column", "column_number": 2},
                {"id": col1.id, "name": "New column", "column_number": 0},
            ],
        )

        # Since column 1 was absent from the update request, it should be gone
        self.assertEqual(result_columns[0].id, col1.id)
        self.assertEqual(result_columns[1].id, col3.id)
        self.assertEqual(len(query.get_columns(user.id)), 2)

    def test_nonexistent_user(self, mock_create_column, mock_delete_column, mock_get_columns):
        mock_get_columns.side_effect = ObjectDoesNotExist("Nonexistant User")
        # User doesn't exist
        with self.assertRaises(ObjectDoesNotExist):
            business.update_columns(
                -1,
                [
                    {"id": -1, "name": "New column", "column_number": 0},
                    {"id": -1, "name": "New column", "column_number": 1},
                ],
            )

    def test_empty_payload(self, mock_create_column, mock_delete_column, mock_get_columns):
        mock_get_columns.return_value = KanbanColumn.objects.none()

        user = UserFactory()
        KanbanColumnFactory(user=user, column_number=1)
        KanbanColumnFactory(user=user, column_number=2)

        # If the user has columns, an empty update should delete all of them
        result_columns = business.update_columns(user.id, [])
        self.assertEqual(len(result_columns), 0)
        self.assertEqual(len(query.get_columns(user.id)), 0)

        # After that, an empty update shouldn't do anything
        result_columns = business.update_columns(user.id, [])
        self.assertEqual(len(result_columns), 0)
        self.assertEqual(len(query.get_columns(user.id)), 0)

    def test_validation(self, mock_create_column, mock_delete_column, mock_get_columns):
        user = UserFactory()
        mock_get_columns.side_effect = ValueError("Error")
        with self.assertRaises(ValueError):
            business.update_columns(
                user.id,
                [
                    {"name": "New column", "column_number": 0},
                ],
            )
        with self.assertRaises(ValueError):
            business.update_columns(
                user.id,
                [
                    {"id": -1, "column_number": 0},
                ],
            )
        with self.assertRaises(ValueError):
            business.update_columns(
                user.id,
                [
                    {
                        "id": -1,
                        "name": "New column",
                    },
                ],
            )
