from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from job import query, models
from job.tests.factories import JobFactory, ReviewRequestFactory
from account.tests.factories import UserFactory
from column.tests.factories import KanbanColumnFactory


class GetOrCreateJobTests(TestCase):
    def test_create_and_get_job(self):
        # first create a user and a column
        user = UserFactory(google_id=4)
        new_column = KanbanColumnFactory(user=user)

        # test creating and getting a job for that user in that column
        job = query.create_job(
            {
                "kcolumn_id": new_column.id,
                "user_id": user.id,
                "position_title": "Manager",
                "company": "The Foundation",
            }
        )
        self.assertEqual(models.Job.objects.count(), 1)

        get_job = query.get_job_by_id(in_user=user.id, job_id=job.id)
        self.assertDictEqual(
            get_job.to_dict(),
            {
                "id": get_job.id,
                "position_title": "Manager",
                "company": "The Foundation",
                "description": "",
                "notes": "",
                "cover_letter": "",
                "kcolumn_id": job.kcolumn.id,
                "user_id": user.id,
                "deadlines": None,
                "type": None,
            },
        )

    def test_invalid_job_get(self):
        JobFactory()
        self.assertEqual(models.Job.objects.count(), 1)
        # test invalid getting
        with self.assertRaises(ObjectDoesNotExist):
            query.get_job_by_id(999, 999)


class JobExistsTests(TestCase):
    def test_job_exists(self):
        job = JobFactory()
        self.assertTrue(query.job_exists(job.id))


class UpdateJobTests(TestCase):
    def test_update_job(self):
        job = JobFactory()
        query.update_job({"id": job.id, "description": "Manage things and stuff"})
        # unsure how to mock get_job_by_id without making the test trivial
        self.assertEqual(query.get_job_by_id(job.user.id, job.id).description, "Manage things and stuff")

    def test_invalid_update_job(self):
        job = JobFactory()

        with self.assertRaises(AttributeError):
            query.update_job({"id": job.id, "start_date": "tomorrow"})

        with self.assertRaises(ObjectDoesNotExist):
            query.update_job({"id": -1, "description": "Manage things and stuff"})


class GetAllJobsTests(TestCase):
    def test_get_minimum_jobs(self):
        job_one = JobFactory()
        job_two = JobFactory(user=job_one.user)
        job_three = JobFactory(user=job_one.user)

        jobs = {job_one.id, job_two.id, job_three.id}
        jobList = list(query.get_minimum_jobs(job_one.user.id))

        self.assertEqual(len(jobList), 3)
        for currJob in jobList:
            self.assertIn(currJob["id"], jobs)


class DeleteJobTests(TestCase):
    def test_job_deletion(self):
        # create job
        mocked_job = JobFactory()

        # test delete job
        self.assertEqual(models.Job.objects.count(), 1)
        query.delete_job(mocked_job.user.id, mocked_job.id)
        self.assertEqual(models.Job.objects.count(), 0)

    def test_invalid_job_deletion(self):
        # create job
        self.assertEqual(models.Job.objects.count(), 0)
        JobFactory()

        with self.assertRaises(ObjectDoesNotExist):
            query.delete_job(-1, -1)

        self.assertEqual(models.Job.objects.count(), 1)


class CreateReviewRequestTests(TestCase):
    def test_create_review_request(self):
        job = JobFactory()
        message = "You should review my cover letter... NOW!"
        payload = {"job_id": job.id, "message": message}

        review_request = query.create_review_request(payload)
        self.assertEqual(review_request.job_id, job.id)
        self.assertEqual(review_request.message, message)
        self.assertEqual(review_request.fulfilled, False)

    def test_invalid_create_review_request(self):
        # Payload has missing fields
        with self.assertRaises(KeyError):
            query.create_review_request({})

        # Job doesn't exist
        message = "Like and subscribe for more cover letters"
        payload_nonexistent_job = {"job_id": -1, "reviewer_id": -1, "message": message}
        with self.assertRaises(ObjectDoesNotExist):
            query.create_review_request(payload_nonexistent_job)


class CreateReviewTests(TestCase):
    def test_create_review(self):
        reviewer = UserFactory()
        request = ReviewRequestFactory()
        response = "2/10 has a little something for everyone"
        payload = {"reviewer_id": reviewer.id, "request_id": request.id, "response": response}

        review = query.create_review(payload)
        self.assertEqual(review.reviewer_id, reviewer.id)
        self.assertEqual(review.request_id, request.id)
        self.assertEqual(review.response, response)
        self.assertEqual(review.completed, None)

    def test_invalid_create_review(self):
        # Payload has missing fields
        with self.assertRaises(KeyError):
            query.create_review({})

        # User doesn't exist
        request = ReviewRequestFactory()
        response = "sorry can't review this i don't exist"
        payload_nonexistent_user = {"reviewer_id": -1, "request_id": request.id, "response": response}
        with self.assertRaises(ObjectDoesNotExist):
            query.create_review(payload_nonexistent_user)

        # Request doesn't exist
        user = UserFactory()
        payload_nonexistent_request = {"reviewer_id": user.id, "request_id": -1, "response": response}
        with self.assertRaises(ObjectDoesNotExist):
            query.create_review(payload_nonexistent_request)


class GetReviewsForUserTests(TestCase):
    def test_get_reviews_for_user(self):
        request = ReviewRequestFactory()
        reviewer = UserFactory()
        review = models.Review.objects.create(reviewer=reviewer, request=request)
        additional_review = models.Review.objects.create(reviewer=reviewer, request=request)
        irrelevant_request = ReviewRequestFactory()
        irrelevant_review = models.Review.objects.create(reviewer=reviewer, request=irrelevant_request)

        reviews = query.get_reviews_for_user({"user_id": request.job.user.id})
        self.assertIn(review, reviews)
        self.assertIn(additional_review, reviews)
        # That query should only get reviews for the given user
        self.assertNotIn(irrelevant_review, reviews)

        # The reviews aren' addressed to the user who wrote them
        reviews_to_reviewer = query.get_reviews_for_user({"user_id": reviewer.id})
        self.assertEqual(len(reviews_to_reviewer), 0)

    def test_invalid_get_reviews_for_user(self):
        # User doesn't exist
        with self.assertRaises(ObjectDoesNotExist):
            query.get_reviews_for_user({"user_id": -1})

        # User not specified
        with self.assertRaises(KeyError):
            query.get_reviews_for_user({})
