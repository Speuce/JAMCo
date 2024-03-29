import json
from unittest.mock import patch, MagicMock

patch("account.decorators.requires_login", lambda *args, **kwargs: lambda x: x).start()

from django.test import RequestFactory, TestCase  # noqa: E402
from django.core.exceptions import ObjectDoesNotExist  # noqa: E402
from job import views  # noqa: E402
from job.tests.factories import JobFactory, ReviewRequestFactory, ReviewFactory  # noqa: E402
from account.tests.factories import UserFactory  # noqa: E402


class TestViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch("job.business.get_minimum_jobs")
    def test_get_minimum_jobs(self, mock_get_minimum_jobs):
        # Prepare data
        user_id = 123
        request_body = json.dumps({"user_id": user_id}).encode("utf-8")
        request = self.factory.post("/get_minimum_jobs/", data=request_body, content_type="application/json")

        # Set up mock
        jobs = [{"id": 1, "position": "Developer", "company": "Google"}]
        mock_get_minimum_jobs.return_value = jobs

        # Call the view function
        response = views.get_minimum_jobs(request)

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), json.dumps({"jobs": jobs}))

    @patch("job.business.get_job_by_id")
    def test_get_job_by_id(self, mock_get_job_by_id):
        # Prepare data
        user_id = 123
        job_id = 456
        request_body = json.dumps({"user_id": user_id, "job_id": job_id}).encode("utf-8")
        request = self.factory.post("/get_job_by_id/", data=request_body, content_type="application/json")

        # Set up mock
        job = MagicMock(
            to_dict=MagicMock(
                return_value={
                    "id": job_id,
                    "position": "Developer",
                    "company": "Google",
                }
            )
        )
        mock_get_job_by_id.return_value = job

        # Call the view function
        response = views.get_job_by_id(request)

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), json.dumps({"job_data": job.to_dict()}))

    @patch("job.business.create_job")
    def test_create_job(self, mock_create_job):
        # Prepare data
        job_data = {"position": "Developer", "company": "Google"}
        request_body = json.dumps(job_data).encode("utf-8")
        request = self.factory.post("/create_job/", data=request_body, content_type="application/json")

        # Set up mock
        job = MagicMock(to_dict=MagicMock(return_value={**job_data, "id": 1}))
        mock_create_job.return_value = job

        # Call the view function
        response = views.create_job(request)

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), json.dumps({"job": job.to_dict()}))

    @patch("job.business.update_job")
    def test_update_job(self, mock_update_job):
        # Prepare data
        job_data = {"id": 1, "position": "Developer", "company": "Google"}
        request_body = json.dumps(job_data).encode("utf-8")
        request = self.factory.post("/update_job/", data=request_body, content_type="application/json")

        # Call the view function
        response = views.update_job(request)
        mock_update_job.assert_called_with(job_data)

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), json.dumps({}))

    @patch("job.business.get_minimum_jobs")
    def test_get_minimum_jobs_with_error(self, mock_get_minimum_jobs):
        mock_get_minimum_jobs.side_effect = Exception("Something went wrong!")
        # Prepare data
        user_id = 123
        request_body = json.dumps({"user_id": user_id}).encode("utf-8")
        request = self.factory.post("/get_minimum_jobs/", data=request_body, content_type="application/json")
        response = views.get_minimum_jobs(request)
        self.assertEqual(response.status_code, 400)

    @patch("job.business.get_job_by_id")
    def test_get_job_by_id_with_error(self, mock_get_job_by_id):
        mock_get_job_by_id.side_effect = Exception("Something went wrong!")
        user_id = 123
        job_id = 456
        request_body = json.dumps({"user_id": user_id, "job_id": job_id}).encode("utf-8")
        request = self.factory.post("/get_job_by_id/", data=request_body, content_type="application/json")

        response = views.get_job_by_id(request)
        self.assertEqual(response.status_code, 400)

    @patch("job.business.create_job")
    def test_create_job_with_error(self, mock_create_job):
        mock_create_job.side_effect = KeyError("Something went wrong!")
        # Prepare data
        job_data = {"position": "Developer", "company": "Google"}
        request_body = json.dumps(job_data).encode("utf-8")
        request = self.factory.post("/create_job/", data=request_body, content_type="application/json")

        # Set up mock
        job = MagicMock(to_dict=MagicMock(return_value={**job_data, "id": 1}))
        mock_create_job.return_value = job
        response = views.create_job(request)
        self.assertEqual(response.status_code, 400)

    @patch("job.business.update_job")
    def test_update_job_with_error(self, mock_update_job):
        mock_update_job.side_effect = ObjectDoesNotExist("Something went wrong!")
        # Prepare data
        job_data = {"id": 1, "position": "Developer", "company": "Google"}
        request_body = json.dumps(job_data).encode("utf-8")
        request = self.factory.post("/update_job/", data=request_body, content_type="application/json")
        response = views.update_job(request)
        mock_update_job.assert_called_with(job_data)
        self.assertEqual(response.status_code, 400)


class ReviewRequestTests(TestCase):
    @patch("job.business.create_review_request")
    def test_create_review_request(self, mock_create_review_request):
        # Prepare data
        review_request_data = {"job_id": JobFactory().id, "message": "i showed you my cover letter please respond"}
        request_body = json.dumps(review_request_data).encode("utf-8")
        request = RequestFactory().post("/create_review_request/", data=request_body, content_type="application/json")

        # Set up mock
        review_request = MagicMock(to_dict=MagicMock(return_value={**review_request_data, "id": 1}))
        mock_create_review_request.return_value = review_request

        # Call the view function
        response = views.create_review_request(request)

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), json.dumps({"review_request": review_request.to_dict()}))

    @patch("job.business.create_review_request")
    def test_create_review_request_with_error(self, mock_create_review_request):
        request_body = json.dumps({}).encode("utf-8")
        request = RequestFactory().post("/create_review_request/", data=request_body, content_type="application/json")

        # Set up mock
        mock_create_review_request.side_effect = Exception("Something went wrong!")

        # Call the view function
        response = views.create_review_request(request)

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode("utf-8"), json.dumps({"error": "Exception('Something went wrong!')"}))

    @patch("job.business.get_review_requests_for_user")
    def test_get_review_requests_for_user(self, mock_get_review_requests_for_user):
        user = UserFactory()
        request_body = json.dumps({"user_id": user.id}).encode("utf-8")
        request = RequestFactory().post(
            "/get_review_requests_for_user/", data=request_body, content_type="application/json"
        )

        review_requests = [ReviewRequestFactory() for i in range(100)]
        mock_get_review_requests_for_user.return_value = review_requests

        response = views.get_review_requests_for_user(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode("utf-8"),
            json.dumps({"review_requests": [review_request.to_dict() for review_request in review_requests]}),
        )

    @patch("job.business.get_review_requests_for_user")
    def test_get_review_requests_for_user_with_error(self, mock_get_review_requests_for_user):
        user = UserFactory()
        request_body = json.dumps({"user_id": user.id}).encode("utf-8")
        request = RequestFactory().post(
            "/get_review_requests_for_user/", data=request_body, content_type="application/json"
        )

        mock_get_review_requests_for_user.side_effect = Exception("Something went wrong!")

        response = views.get_review_requests_for_user(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode("utf-8"), json.dumps({"error": "Exception('Something went wrong!')"}))


class ReviewTests(TestCase):
    @patch("job.business.create_review")
    def test_create_review(self, mock_create_review):
        review_data = {
            "reviewer_id": UserFactory().id,
            "request_id": ReviewRequestFactory().id,
            "response": "best cover letter I've ever seen 10/10",
            "completed": None,
        }

        request_body = json.dumps(review_data).encode("utf-8")
        request = RequestFactory().post("/create_review/", data=request_body, content_type="application/json")

        review = MagicMock(to_dict=MagicMock(return_value={**review_data, "id": 1}))
        mock_create_review.return_value = review

        response = views.create_review(request)

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), json.dumps({"review": review.to_dict()}))

    @patch("job.business.create_review")
    def test_create_review_with_error(self, mock_create_review):
        request_body = json.dumps({}).encode("utf-8")
        request = RequestFactory().post("/create_review/", data=request_body, content_type="application/json")

        # Set up mock
        mock_create_review.side_effect = Exception("Something went wrong!")

        # Call the view function
        response = views.create_review(request)

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode("utf-8"), json.dumps({"error": "Exception('Something went wrong!')"}))

    @patch("job.business.get_reviews_for_user")
    def test_get_reviews_for_user(self, mock_get_reviews_for_user):
        user = UserFactory()
        request_body = json.dumps({"user_id": user.id}).encode("utf-8")
        request = RequestFactory().post("/get_reviews_for_user/", data=request_body, content_type="application/json")

        # In the situation we're modelling, one user reviewed that cover letter an incredible number of times
        reviews = [ReviewFactory() for i in range(100)]
        mock_get_reviews_for_user.return_value = reviews

        response = views.get_reviews_for_user(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode("utf-8"), json.dumps({"reviews": [review.to_dict() for review in reviews]})
        )

    @patch("job.business.get_reviews_for_user")
    def test_get_reviews_for_user_with_error(self, mock_get_reviews_for_user):
        user = UserFactory()
        request_body = json.dumps({"user_id": user.id}).encode("utf-8")
        request = RequestFactory().post("/get_reviews_for_user/", data=request_body, content_type="application/json")

        mock_get_reviews_for_user.side_effect = Exception("Something went wrong!")

        response = views.get_reviews_for_user(request)

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode("utf-8"), json.dumps({"error": "Exception('Something went wrong!')"}))
