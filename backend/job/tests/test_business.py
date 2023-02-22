import json
from django.test import TransactionTestCase
from unittest.mock import patch
from job import business, query
from job.tests.factories import JobFactory
from account import query as account_query
from column import query as column_query


class CreateJobTests(TransactionTestCase):
    @patch("job.query.create_job")
    @patch("job.query.get_job_by_id")
    def test_create_job(self, mock_create_job, mock_get_job_by_id):
        mocked_job = JobFactory()

        mock_create_job.return_value = mocked_job
        mock_get_job_by_id.return_value = mocked_job

        job = {"id": -1, "user_id": mocked_job.user.id, "kcolumn_id": mocked_job.kcolumn.id}

        job_create = business.create_job(job)
        job_get = business.get_job_by_id(mocked_job.user.id, job_create.id)

        self.assertEqual(job_create.to_dict(), job_get.to_dict())


class UpdateJobTest(TransactionTestCase):
    @patch("job.query.get_job_by_id")
    @patch("job.query.update_job")
    def test_update_job(self, mock_get_job_by_id, mock_update_job):
        mocked_job = JobFactory.build()
        mock_get_job_by_id.return_value = mocked_job
        mock_update_job.return_value = mocked_job

        update_job = {
            "id": 0,
            "position_title": "pos",
            "company": "company",
        }

        business.update_job(update_job)

        get_job = business.get_job_by_id(mocked_job.user.id, mocked_job.id)
        self.assertEqual(mocked_job.to_dict(), get_job.to_dict())


class GetMinimumJobsTests(TransactionTestCase):
    reset_sequences = True

    def test_get_minimum_jobs(self):
        user = account_query.get_or_create_user({"sub": "4"})
        column = column_query.create_column(user.id, "New column", 0)

        jobs = [
            {
                "id": -1,
                "user_id": user.id,
                "kcolumn_id": column.id,
                "position_title": "pos",
                "company": "com",
                "type": "ty",
            },
            {
                "id": -1,
                "user_id": user.id,
                "kcolumn_id": column.id,
                "position_title": "position",
                "company": "com",
                "type": "ty",
            },
            {
                "id": -1,
                "user_id": user.id,
                "kcolumn_id": column.id,
                "position_title": "pose",
                "company": "comp",
                "notes": "notes",
            },
        ]

        min_jobs = [
            {
                "id": 1,
                "kcolumn": column.id,
                "position_title": "pos",
                "company": "com",
                "type": "ty",
            },
            {
                "id": 2,
                "kcolumn": column.id,
                "position_title": "position",
                "company": "com",
                "type": "ty",
            },
            {
                "id": 3,
                "kcolumn": column.id,
                "position_title": "pose",
                "company": "comp",
                "type": None,
            },
        ]

        query.create_job(jobs[0])
        query.create_job(jobs[1])
        query.create_job(jobs[2])

        min_jobs_response = business.get_minimum_jobs(user.id)

        self.assertEqual(json.dumps(list(min_jobs)), json.dumps(list(min_jobs_response)))


class GetJobByIdTests(TransactionTestCase):
    def test_get_job_by_id(self):
        user = account_query.get_or_create_user({"sub": "4"})
        column = column_query.create_column(user.id, "New column", 0)

        jobs = [
            {
                "id": 1,
                "user_id": user.id,
                "kcolumn_id": column.id,
                "position_title": "pos",
                "company": "com",
                "type": "ty",
                "cover_letter": "cover",
                "notes": "notes",
                "description": "desc",
                "deadlines": None,
            },
            {
                "id": 2,
                "user_id": user.id,
                "kcolumn_id": column.id,
                "position_title": "position",
                "company": "com",
                "type": "ty",
                "cover_letter": "cover",
                "notes": "notes",
                "description": "desc",
                "deadlines": None,
            },
        ]

        job_one_create = business.create_job(jobs[0])
        job_two_create = business.create_job(jobs[1])

        job_one = business.get_job_by_id(user.id, job_one_create.id)
        self.assertEqual(job_one_create.to_dict(), job_one.to_dict())

        job_two = business.get_job_by_id(user.id, job_two_create.id)
        self.assertEqual(job_two_create.to_dict(), job_two.to_dict())
