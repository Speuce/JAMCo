import json
from django.test import TransactionTestCase
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from job import business, query
from account import query as account_query


class CreateJobTests(TransactionTestCase):

    def test_create_job(self):
        user = account_query.get_or_create_user({"sub": "4"})
        column = account_query.create_column(user.id, "New column", 0)

        jobs = [
            {
                "id": -1,
                "user_id": user.id,
                "kcolumn_id": column.id,
                "position_title": "pos",
                "company": "com",
                "type": "ty"
            },
            {
                "id": -1,
                "user_id": user.id,
                "kcolumn_id": column.id,
                "position_title": "position",
                "company": "com",
                "type": "ty"
            },
        ]

        job_one_create = business.create_job(jobs[0])
        job_two_create = business.create_job(jobs[1])

        job_one = business.get_job_by_id(user.id, job_one_create.id)
        self.assertEqual(job_one_create.to_dict(), job_one.to_dict())

        job_two = business.get_job_by_id(user.id, job_two_create.id)
        self.assertEqual(job_two_create.to_dict(), job_two.to_dict())


class GetMinimumJobsTests(TransactionTestCase):
    reset_sequences = True

    def test_get_minimum_jobs(self):
        user = account_query.get_or_create_user({"sub": "4"})
        column = account_query.create_column(user.id, "New column", 0)

        jobs = [{
            "id": -1,
            "user_id": user.id,
            "kcolumn_id": column.id,
            "position_title": "pos",
            "company": "com",
            "type": "ty"
        }, {
            "id": -1,
            "user_id": user.id,
            "kcolumn_id": column.id,
            "position_title": "position",
            "company": "com",
            "type": "ty"
        }, {
            "id": -1,
            "user_id": user.id,
            "kcolumn_id": column.id,
            "position_title": "pose",
            "company": "comp",
            "notes": "notes"
        }]

        min_jobs = [{
            "id": 1,
            "kcolumn": column.id,
            "position_title": "pos",
            "company": "com",
            "type": "ty"
        }, {
            "id": 2,
            "kcolumn": column.id,
            "position_title": "position",
            "company": "com",
            "type": "ty"
        }, {
            "id": 3,
            "kcolumn": column.id,
            "position_title": "pose",
            "company": "comp",
            "type": None
        }]

        query.create_job(jobs[0])
        query.create_job(jobs[1])
        query.create_job(jobs[2])

        min_jobs_response = business.get_minimum_jobs(user.id)

        # this test fails
        # something funky with the get_minimum_jobs return value formatting
        self.assertEqual(json.dumps(list(min_jobs)),
                         json.dumps(list(min_jobs_response)))


class GetJobByIdTests(TransactionTestCase):

    def test_get_job_by_id(self):
        user = account_query.get_or_create_user({"sub": "4"})
        column = account_query.create_column(user.id, "New column", 0)

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
                "deadlines": None
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
                "deadlines": None
            },
        ]

        job_one_create = business.create_job(jobs[0])
        job_two_create = business.create_job(jobs[1])

        job_one = business.get_job_by_id(user.id, job_one_create.id)
        self.assertEqual(job_one_create.to_dict(), job_one.to_dict())

        job_two = business.get_job_by_id(user.id, job_two_create.id)
        self.assertEqual(job_two_create.to_dict(), job_two.to_dict())
