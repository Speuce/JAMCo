import logging
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from job import query as jquery, models as jmodels
from account import query as aquery, models as amodels

logger = logging.getLogger(__name__)


class GetOrCreateJobTests(TestCase):
    def test_create_and_get_job(self):
        # 'sub' is the field name from google tokens
        user = aquery.get_or_create_user({"sub": "4"})
        # A user should exist after that query
        self.assertTrue(amodels.User.objects.filter(google_id="4").exists())

        # test creating and getting a job for that user
        job = jquery.create_job(
            {
                "user_id": user.id,
                "position_title": "Manager",
                "company": "The Foundation",
            }
        )
        # should be the first job, and should exist
        self.assertEqual(jmodels.Job.objects.count(), 1)
