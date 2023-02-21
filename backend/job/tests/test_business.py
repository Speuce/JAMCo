import json
from django.test import TransactionTestCase
from job import business, query
from account import query as account_query
from column import query as column_query
from job import models


class CreateJobTests(TransactionTestCase):
    def test_create_job(self):
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
        ]

        job_one_create = business.create_job(jobs[0])
        job_two_create = business.create_job(jobs[1])

        job_one = business.get_job_by_id(user.id, job_one_create.id)
        self.assertEqual(job_one_create.to_dict(), job_one.to_dict())

        job_two = business.get_job_by_id(user.id, job_two_create.id)
        self.assertEqual(job_two_create.to_dict(), job_two.to_dict())


class UpdateJobTest(TransactionTestCase):
    def test_update_job(self):
        user = account_query.get_or_create_user({"sub": "4"})
        column = column_query.create_column(user.id, "New column", 0)

        job = {
            "id": -1,
            "user_id": user.id,
            "kcolumn_id": column.id,
            "position_title": "pos",
            "company": "com",
            "type": "ty",
        }

        job_created = business.create_job(job)

        update_job = {
            "id": job_created.id,
            "kcolumn_id": column.id,
            "position_title": "new position",
            "company": "company",
            "type": None,
        }

        business.update_job(update_job)

        updated_model = models.Job.objects.create(
            type=None,
            kcolumn=models.KanbanColumn(column.id),
            user=user,
            position_title="new position",
            company="company",
            description="",
            notes="",
            cover_letter="",
            deadlines=None,
        )

        updated_model_dict = updated_model.to_dict()
        updated_model_dict["id"] = 4

        get_job_dict = business.get_job_by_id(user.id, job_created.id).to_dict()
        self.assertEqual(updated_model_dict, get_job_dict)


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
