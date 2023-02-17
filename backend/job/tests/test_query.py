import logging
from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ObjectDoesNotExist
from job import query as jquery, models as jmodels
from account import query as aquery, models as amodels

logger = logging.getLogger(__name__)


class GetOrCreateJobTests(TransactionTestCase):
    def test_create_and_get_job(self):
        # first create a user and a column
        user = aquery.get_or_create_user({"sub": "4"})
        new_column = aquery.create_column(user.id, "New column", 0)

        # test creating and getting a job for that user in that column
        new_job = jquery.create_job(
            {
                "kcolumn_id": new_column.id,
                "user_id": user.id,
                "position_title": "Manager",
                "company": "The Foundation",
            }
        )
        # should be the first job, and should exist
        self.assertEqual(jmodels.Job.objects.count(), 1)

        get_job = jquery.get_job_by_id(in_user=user.id, job_id=new_job.id)
        self.assertDictEqual(
            get_job.to_dict(),
            {
                "id": get_job.id,
                "position_title": "Manager",
                "company": "The Foundation",
                "description": "",
                "notes": "",
                "cover_letter": "",
                "kcolumn_id": new_column.id,
                "deadlines": None,
                "type":None,
            },
        )

    def test_invalid_get(self):
        # first create a user and a column
        user = aquery.get_or_create_user({"sub": "5"})
        new_column = aquery.create_column(user.id, "New column", 0)

        # test creating and getting a job for that user in that column
        new_job = jquery.create_job(
            {
                "kcolumn_id": new_column.id,
                "user_id": user.id,
                "position_title": "Manager",
                "company": "The Foundation",
            }
        )

        # the invalid getting:
        with self.assertRaises(ObjectDoesNotExist):
            jquery.get_job_by_id(999, 999)


class JobExistsTests(TransactionTestCase):
    def test_job_exists(self):
        # first create a user and a column
        user = aquery.get_or_create_user({"sub": "6"})
        new_column = aquery.create_column(user.id, "New column", 0)

        # test creating and getting a job for that user in that column
        new_job = jquery.create_job(
            {
                "kcolumn_id": new_column.id,
                "user_id": user.id,
                "position_title": "Manager",
                "company": "The Foundation",
            }
        )

        self.assertTrue(jquery.job_exists(new_job.id))


class UpdateJobTests(TransactionTestCase):
    def test_update_job(self):
        # first create a user and a column
        user = aquery.get_or_create_user({"sub": "7"})
        new_column = aquery.create_column(user.id, "New column", 0)

        # test creating and getting a job for that user in that column
        job = jquery.create_job(
            {
                "kcolumn_id": new_column.id,
                "user_id": user.id,
                "position_title": "Manager",
                "company": "The Foundation",
            }
        )

        jquery.update_job({"id": job.id, "description": "Manage things and stuff"})
        self.assertEqual(
            jquery.get_job_by_id(user.id, job.id).description, "Manage things and stuff"
        )

    def test_invalid_update_job(self):
        # first create a user and a column
        user = aquery.get_or_create_user({"sub": "8"})
        new_column = aquery.create_column(user.id, "New column", 0)

        # test creating and getting a job for that user in that column
        job = jquery.create_job(
            {
                "kcolumn_id": new_column.id,
                "user_id": user.id,
                "position_title": "Manager",
                "company": "The Foundation",
            }
        )

        with self.assertRaises(AttributeError):
            jquery.update_job({"id": job.id, "start_date": "tomorrow"})

        with self.assertRaises(ObjectDoesNotExist):
            jquery.update_job({"id": -1, "description": "Manage things and stuff"})


class GetAllJobsTests(TransactionTestCase):
    def test_get_minimum_jobs(self):
        # first create a user and a column
        user = aquery.get_or_create_user({"sub": "10"})
        column1 = aquery.create_column(user.id, "New column", 0)
        column2 = aquery.create_column(user.id, "Newer column", 1)

        # test creating and getting a job for that user in that column
        job1 = jquery.create_job(
            {
                "kcolumn_id": column1.id,
                "user_id": user.id,
                "position_title": "Manager",
                "company": "The Foundation",
            }
        )
        job2 = jquery.create_job(
            {
                "kcolumn_id": column2.id,
                "user_id": user.id,
                "position_title": "Managerial",
                "company": "The Foundation",
            }
        )
        job3 = jquery.create_job(
            {
                "kcolumn_id": column2.id,
                "user_id": user.id,
                "position_title": "Sub-Manager",
                "company": "The Foundation",
            }
        )

        jobs = {job1.id, job2.id, job3.id}
        jobList = list(jquery.get_minimum_jobs(user.id))

        self.assertEqual(len(jobList), 3)
        for currJob in jobList:
            self.assertIn(currJob["id"], jobs)


class DeleteJobTests(TransactionTestCase):
    def test_job_deletion(self):
        # first create a user and a column
        user = aquery.get_or_create_user({"sub": "11"})
        column = aquery.create_column(user.id, "New column", 0)

        # test creating and getting a job for that user in that column
        job = jquery.create_job(
            {
                "kcolumn_id": column.id,
                "user_id": user.id,
                "position_title": "Manager",
                "company": "The Foundation",
            }
        )

        jquery.delete_job(user.id, job.id)
        self.assertEqual(jmodels.Job.objects.count(), 0)

    def test_invalid_job_deletion(self):
        # first create a user and a column
        user = aquery.get_or_create_user({"sub": "11"})
        column = aquery.create_column(user.id, "New column", 0)

        # test creating and getting a job for that user in that column
        job = jquery.create_job(
            {
                "kcolumn_id": column.id,
                "user_id": user.id,
                "position_title": "Manager",
                "company": "The Foundation",
            }
        )

        with self.assertRaises(ObjectDoesNotExist):
            jquery.delete_job(-1, -1)

        self.assertEqual(jmodels.Job.objects.count(), 1)
