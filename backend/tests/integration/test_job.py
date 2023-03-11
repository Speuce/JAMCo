import json
from django.test import TransactionTestCase
from django.urls import reverse
from job.models import Job, ReviewRequest, Review
from account.tests.factories import UserFactory
from column.tests.factories import KanbanColumnFactory
from job.tests.factories import JobFactory, ReviewRequestFactory


class TestViews(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user = UserFactory()
        self.column = KanbanColumnFactory(user=self.user)

    def test_create_job(self):
        self.assertEqual(len(Job.objects.all()), 0)
        # Prepare data
        job_data = {
            "position_title": "Developer",
            "company": "Google",
            "kcolumn_id": self.column.id,
            "user_id": self.user.id,
        }

        response = self.client.post(
            reverse("create_job"),
            json.dumps(job_data),
            content_type="application/json",
        )

        # Check the response

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Job.objects.all()), 1)
        self.assertEqual(
            json.loads(response.content)["job"],
            {
                "id": 1,
                "position_title": "Developer",
                "company": "Google",
                "description": "",
                "notes": "",
                "cover_letter": "",
                "kcolumn_id": 1,
                "deadlines": None,
                "type": None,
            },
        )

    def test_create_job_with_error(self):
        self.assertEqual(len(Job.objects.all()), 0)
        # Prepare data missing user_id
        job_data = {
            "company": "Google",
            "kcolumn_id": self.column.id,
            "position_title": "Developer",
        }

        response = self.client.post(
            reverse("create_job"),
            json.dumps(job_data),
            content_type="application/json",
        )

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(Job.objects.all()), 0)

        # Prepare data missing position_title
        job_data = {
            "company": "Google",
            "kcolumn_id": self.column.id,
            "user_id": self.user.id,
        }

        response = self.client.post(
            reverse("create_job"),
            json.dumps(job_data),
            content_type="application/json",
        )

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(Job.objects.all()), 0)

        # Prepare data missing kcolumn_id
        job_data = {"company": "Google", "user_id": self.user.id, "position_title": "title"}

        response = self.client.post(
            reverse("create_job"),
            json.dumps(job_data),
            content_type="application/json",
        )

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(Job.objects.all()), 0)

        # Prepare data missing company
        job_data = {"user_id": self.user.id, "kcolumn_id": self.column.id, "position_title": "title"}

        response = self.client.post(
            reverse("create_job"),
            json.dumps(job_data),
            content_type="application/json",
        )

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(Job.objects.all()), 0)

    def test_update_job(self):
        self.assertEqual(len(Job.objects.all()), 0)
        # Create Job
        job_data = {
            "position_title": "Developer",
            "company": "Google",
            "kcolumn_id": self.column.id,
            "user_id": self.user.id,
        }

        response = self.client.post(
            reverse("create_job"),
            json.dumps(job_data),
            content_type="application/json",
        )

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Job.objects.all()), 1)
        self.assertEqual(
            json.loads(response.content)["job"],
            {
                "id": 1,
                "position_title": "Developer",
                "company": "Google",
                "description": "",
                "notes": "",
                "cover_letter": "",
                "kcolumn_id": self.column.id,
                "deadlines": None,
                "type": None,
            },
        )

        # Update Job
        updated_job_data = {
            "id": 1,
            "company": "Gooble",
            "kcolumn_id": self.column.id,
            "user_id": self.user.id,
            "position_title": "Dev",
            "type": "test_type",
            "cover_letter": "cover letter",
        }

        response = self.client.post(
            reverse("update_job"),
            json.dumps(updated_job_data),
            content_type="application/json",
        )

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Job.objects.all()), 1)
        self.assertEqual(response.content.decode("utf-8"), json.dumps({}))

        self.assertEqual(
            Job.objects.get(id=1).to_dict(),
            {
                "id": 1,
                "position_title": "Dev",
                "company": "Gooble",
                "description": "",
                "notes": "",
                "cover_letter": "cover letter",
                "kcolumn_id": self.column.id,
                "deadlines": None,
                "type": "test_type",
            },
        )

    def test_update_job_with_invalid_field_error(self):
        self.assertEqual(len(Job.objects.all()), 0)
        # Create Job
        job_data = {
            "position_title": "Developer",
            "company": "Google",
            "kcolumn_id": self.column.id,
            "user_id": self.user.id,
        }

        response = self.client.post(
            reverse("create_job"),
            json.dumps(job_data),
            content_type="application/json",
        )

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Job.objects.all()), 1)
        self.assertEqual(
            json.loads(response.content)["job"],
            {
                "id": 1,
                "position_title": "Developer",
                "company": "Google",
                "description": "",
                "notes": "",
                "cover_letter": "",
                "kcolumn_id": self.column.id,
                "deadlines": None,
                "type": None,
            },
        )

        # Update Job
        updated_job_data = {
            "id": 1,
            "invalid": "Gooble",
            "kcolumn_id": self.column.id,
            "user_id": self.user.id,
            "position_title": "Dev",
            "type": "test_type",
            "cover_letter": "cover letter",
        }

        response = self.client.post(
            reverse("update_job"),
            json.dumps(updated_job_data),
            content_type="application/json",
        )

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(Job.objects.all()), 1)
        self.assertEqual(
            response.content.decode("utf-8"),
            json.dumps({"error": "AttributeError('Job has no attribute invalid')"}),
        )

        self.assertEqual(
            Job.objects.get(id=1).to_dict(),
            {
                "id": 1,
                "position_title": "Developer",
                "company": "Google",
                "description": "",
                "notes": "",
                "cover_letter": "",
                "kcolumn_id": self.column.id,
                "deadlines": None,
                "type": None,
            },
        )

    def test_update_job_with_invalid_id_error(self):
        self.assertEqual(len(Job.objects.all()), 0)
        # Create Job
        job_data = {
            "position_title": "Developer",
            "company": "Google",
            "kcolumn_id": self.column.id,
            "user_id": self.user.id,
        }

        response = self.client.post(
            reverse("create_job"),
            json.dumps(job_data),
            content_type="application/json",
        )

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Job.objects.all()), 1)
        self.assertEqual(
            json.loads(response.content)["job"],
            {
                "id": 1,
                "position_title": "Developer",
                "company": "Google",
                "description": "",
                "notes": "",
                "cover_letter": "",
                "kcolumn_id": self.column.id,
                "deadlines": None,
                "type": None,
            },
        )

        # Update Job
        updated_job_data = {
            "id": 2,
            "invalid": "Gooble",
            "kcolumn_id": self.column.id,
            "user_id": self.user.id,
            "position_title": "Dev",
            "type": "test_type",
            "cover_letter": "cover letter",
        }

        response = self.client.post(
            reverse("update_job"),
            json.dumps(updated_job_data),
            content_type="application/json",
        )

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(Job.objects.all()), 1)
        self.assertEqual(
            response.content.decode("utf-8"),
            json.dumps({"error": "DoesNotExist('Job matching query does not exist.')"}),
        )

        self.assertEqual(
            Job.objects.get(id=1).to_dict(),
            {
                "id": 1,
                "position_title": "Developer",
                "company": "Google",
                "description": "",
                "notes": "",
                "cover_letter": "",
                "kcolumn_id": self.column.id,
                "deadlines": None,
                "type": None,
            },
        )

    def test_get_minimum_jobs(self):
        self.assertEqual(len(Job.objects.all()), 0)
        # Create Job
        job_data = {
            "position_title": "Developer",
            "company": "Google",
            "kcolumn_id": self.column.id,
            "user_id": self.user.id,
        }

        response = self.client.post(
            reverse("create_job"),
            json.dumps(job_data),
            content_type="application/json",
        )

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Job.objects.all()), 1)
        self.assertEqual(
            json.loads(response.content)["job"],
            {
                "id": 1,
                "position_title": "Developer",
                "company": "Google",
                "description": "",
                "notes": "",
                "cover_letter": "",
                "kcolumn_id": self.column.id,
                "deadlines": None,
                "type": None,
            },
        )

        # Get Min Jobs
        response = self.client.post(
            reverse("get_minimum_jobs"),
            json.dumps({"user_id": self.user.id}),
            content_type="application/json",
        )

        jobs = [{"id": 1, "kcolumn": self.column.id, "position_title": "Developer", "company": "Google", "type": None}]

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), json.dumps({"jobs": jobs}))

    def test_get_minimum_jobs_nonexistent_user(self):
        # Get Min Jobs
        response = self.client.post(
            reverse("get_minimum_jobs"),
            json.dumps({"user_id": 2}),
            content_type="application/json",
        )

        jobs = []

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), json.dumps({"jobs": jobs}))

    def test_get_job_by_id(self):
        self.assertEqual(len(Job.objects.all()), 0)
        # Create Job
        job_data = {
            "position_title": "Developer",
            "company": "Google",
            "kcolumn_id": self.column.id,
            "user_id": self.user.id,
        }

        response = self.client.post(
            reverse("create_job"),
            json.dumps(job_data),
            content_type="application/json",
        )

        response_json = {
            "id": 1,
            "position_title": "Developer",
            "company": "Google",
            "description": "",
            "notes": "",
            "cover_letter": "",
            "kcolumn_id": self.column.id,
            "deadlines": None,
            "type": None,
        }

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Job.objects.all()), 1)
        self.assertEqual(
            json.loads(response.content)["job"],
            response_json,
        )

        # Get Job
        response = self.client.post(
            reverse("get_job_by_id"),
            json.dumps({"user_id": self.user.id, "job_id": 1}),
            content_type="application/json",
        )

        # Check the response
        self.assertEqual(len(Job.objects.all()), 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), json.dumps({"job_data": response_json}))

    def test_get_job_by_id_with_invalid_user_error(self):
        self.assertEqual(len(Job.objects.all()), 0)
        # Create Job For User 2
        user_two = UserFactory()
        column_two = KanbanColumnFactory(user=user_two)

        job_data = {
            "position_title": "Developer",
            "company": "Google",
            "kcolumn_id": column_two.id,
            "user_id": user_two.id,
        }

        response = self.client.post(
            reverse("create_job"),
            json.dumps(job_data),
            content_type="application/json",
        )

        response_json = {
            "id": 1,
            "position_title": "Developer",
            "company": "Google",
            "description": "",
            "notes": "",
            "cover_letter": "",
            "kcolumn_id": column_two.id,
            "deadlines": None,
            "type": None,
        }

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Job.objects.all()), 1)
        self.assertEqual(
            json.loads(response.content)["job"],
            response_json,
        )

        # Try getting job not associated with User
        response = self.client.post(
            reverse("get_job_by_id"),
            json.dumps({"user_id": self.user.id, "job_id": 1}),
            content_type="application/json",
        )

        # Check the response
        self.assertEqual(len(Job.objects.all()), 1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode("utf-8"),
            json.dumps({"error": "ObjectDoesNotExist('Job with that User does not exist')"}),
        )

    def test_get_job_by_id_invalid_job_error(self):
        self.assertEqual(len(Job.objects.all()), 0)

        # Try getting job which does not exist
        response = self.client.post(
            reverse("get_job_by_id"),
            json.dumps({"user_id": self.user.id, "job_id": 1}),
            content_type="application/json",
        )

        # Check the response
        self.assertEqual(len(Job.objects.all()), 0)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode("utf-8"),
            json.dumps({"error": "ObjectDoesNotExist('Job with that User does not exist')"}),
        )

    def test_create_review_request(self):
        self.assertEqual(len(ReviewRequest.objects.all()), 0)

        job = JobFactory()
        payload = {"job_id": job.id, "message": "i showed you my cover letter please respond"}

        response = self.client.post(
            reverse("create_review_request"),
            json.dumps(payload),
            content_type="application/json",
        )

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(ReviewRequest.objects.all()), 1)
        response_dict = json.loads(response.content)["review_request"]
        self.assertGreaterEqual(response_dict["id"], 0)
        self.assertEqual(response_dict["job_id"], payload["job_id"])
        self.assertEqual(response_dict["message"], payload["message"])
        self.assertEqual(response_dict["fulfilled"], False)

    def test_create_review_with_error(self):
        self.assertEqual(len(Review.objects.all()), 0)

        review_request = ReviewRequestFactory()
        reviewer = UserFactory()

        # Reviewer doesn't exist
        review_data = {"reviewer_id": -1, "request_id": review_request.id, "response": "7.8/10 too much water"}
        response = self.client.post(
            reverse("create_review"),
            json.dumps(review_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(Review.objects.all()), 0)

        # Request doesn't exist
        review_data = {"reviewer_id": reviewer.id, "request_id": -1, "response": "🤓"}
        response = self.client.post(
            reverse("create_review"),
            json.dumps(review_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(Review.objects.all()), 0)

        # Response not given
        review_data = {"reviewer_id": reviewer.id, "request_id": review_request.id}
        response = self.client.post(
            reverse("create_review"),
            json.dumps(review_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(Review.objects.all()), 0)

        # (an empty response is fine, though)
        review_data = {"reviewer_id": reviewer.id, "request_id": review_request.id, "response": ""}
        response = self.client.post(
            reverse("create_review"),
            json.dumps(review_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Review.objects.all()), 1)

        # Field(s) missing
        review_data = {"request_id": review_request.id}
        response = self.client.post(
            reverse("create_review"),
            json.dumps(review_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(Review.objects.all()), 1)
