import json
from django.test import TransactionTestCase
from django.urls import reverse
from job.models import Job, ReviewRequest, Review
from account.tests.factories import UserFactory
from column.tests.factories import KanbanColumnFactory
from job.tests.factories import JobFactory, ReviewRequestFactory, ReviewFactory


class CreateJobTests(TransactionTestCase):
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
                "user_id": self.user.id,
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


class UpdateJobTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user = UserFactory()
        self.column = KanbanColumnFactory(user=self.user)

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
                "user_id": self.user.id,
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
                "user_id": self.user.id,
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
                "user_id": self.user.id,
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
                "user_id": self.user.id,
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
                "user_id": self.user.id,
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
                "user_id": self.user.id,
                "deadlines": None,
                "type": None,
            },
        )


class GetMinimumJobsTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user = UserFactory()
        self.column = KanbanColumnFactory(user=self.user)

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
                "user_id": self.user.id,
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


class GetJobByIdTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user = UserFactory()
        self.column = KanbanColumnFactory(user=self.user)

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
            "user_id": self.user.id,
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
            "user_id": user_two.id,
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
        reviewer = UserFactory()
        payload = {
            "job_id": job.id,
            "reviewer_id": reviewer.id,
            "message": "i showed you my cover letter please respond",
        }

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
        self.assertEqual(response_dict["reviewer_id"], payload["reviewer_id"])
        self.assertEqual(response_dict["job_id"], payload["job_id"])
        self.assertEqual(response_dict["message"], payload["message"])
        self.assertEqual(response_dict["fulfilled"], False)

    def test_create_review_request_with_error(self):
        self.assertEqual(len(ReviewRequest.objects.all()), 0)

        # Payload has missing fields
        response = self.client.post(reverse("create_review_request"), "{}", content_type="application/JSON")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(ReviewRequest.objects.all()), 0)

        # Reviewer doesn't exist
        payload = {"reviewer_id": -1, "message": "7.8/10 too much water?"}
        response = self.client.post(
            reverse("create_review_request"),
            json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(ReviewRequest.objects.all()), 0)

        # Job doesn't exist
        payload = {"job_id": -1, "message": "REVIEW COVER LETTER NOW (2019) (NO VIRUS)"}
        response = self.client.post(
            reverse("create_review_request"),
            json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(ReviewRequest.objects.all()), 0)

    def test_create_review(self):
        self.assertEqual(len(Review.objects.all()), 0)

        review_request = ReviewRequestFactory()
        payload = {"request_id": review_request.id, "response": "W"}

        response = self.client.post(
            reverse("create_review"),
            json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Review.objects.all()), 1)
        response_dict = json.loads(response.content)["review"]
        self.assertGreaterEqual(response_dict["id"], 0)
        self.assertEqual(response_dict["request_id"], payload["request_id"])
        self.assertEqual(response_dict["response"], payload["response"])
        self.assertEqual(response_dict["completed"], None)

    def test_create_review_with_error(self):
        self.assertEqual(len(Review.objects.all()), 0)

        review_request = ReviewRequestFactory()
        reviewer = UserFactory()

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

    def test_get_reviews_for_user(self):
        recipient = UserFactory()
        reviews = [ReviewFactory() for i in range(100)]
        for review in reviews:
            review.request.job.user = recipient
            review.request.job.save()
        other_recipient = UserFactory()
        other_reviews = [ReviewFactory() for i in range(200)]
        for review in other_reviews:
            review.request.job.user = other_recipient
            review.request.job.save()

        payload = {"user_id": recipient.id}

        response = self.client.post(
            reverse("get_reviews_for_user"), json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(Review.objects.count(), 300)
        self.assertEqual(len(json.loads(response.content)["reviews"]), 100)

    def test_get_reviews_for_user_with_error(self):
        # Recipient doesn't exist
        response = self.client.post(
            reverse("get_reviews_for_user"), json.dumps({"user_id": -1}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
