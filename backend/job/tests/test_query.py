import logging
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from job import query as jquery, models as jmodels
from account import query as aquery, models as amodels

logger = logging.getLogger(__name__)


class GetOrCreateJobTests(TestCase):
    def test_create_and_get_job(self):
        # first create a user and a column
        user = aquery.get_or_create_user({"sub": "4"})
        new_column = aquery.create_column(user.id, "New column", 0)

        # test creating and getting a job for that user in that column
        job = jquery.create_job(
            {
                "column_id": new_column.id,
                "user_id": user.id,
                "position_title": "Manager",
                "company": "The Foundation",
            }
        )
        # should be the first job, and should exist
        self.assertEqual(jmodels.Job.objects.count(), 1)
