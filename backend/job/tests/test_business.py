from django.test import TransactionTestCase
from unittest.mock import patch
from job import business
from job.tests.factories import JobFactory


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

    @patch("job.query.get_minimum_jobs")
    def test_get_minimum_jobs(self, mock_get_minimum_jobs):
        job_list = [
            {
                "id": -1,
                "kcolumn_id": 0,
                "position_title": "pos",
                "company": "com",
                "type": "ty",
            },
            {
                "id": -1,
                "kcolumn_id": 0,
                "position_title": "position",
                "company": "com",
                "type": "ty",
            },
        ]
        mock_get_minimum_jobs.return_value = job_list

        min_jobs_response = business.get_minimum_jobs(0)

        self.assertEqual(job_list, min_jobs_response)


class GetJobByIdTests(TransactionTestCase):
    @patch("job.query.get_job_by_id")
    def test_get_job_by_id(self, mock_get_job_by_id):
        mocked_job = JobFactory.build()
        mock_get_job_by_id.return_value = mocked_job

        job_response = business.get_job_by_id(0, mocked_job.id)
        self.assertEqual(mocked_job.to_dict(), job_response.to_dict())
