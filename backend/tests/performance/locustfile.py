from locust import HttpUser, task, between
from faker import Faker
from django.test import TestCase
import json


class UserActor(HttpUser, TestCase):
    wait_time = between(1, 3)

    # simulate login
    def on_start(self):
        self.faker = Faker()

        # get session csrf token
        response = self.client.get("/")
        self.csrftoken = response.cookies["csrftoken"]

        # create account
        response = self.client.post(
            "/account/api/get_or_create_account",
            json.dumps({"credential": "load_test", "client_id": "load_test"}),
            headers={"X-CSRFToken": self.csrftoken},
        )
        if response.status_code != 200:
            raise Exception(f"get_or_create_account error {json.loads(response.content)}")

        content = json.loads(response.content)["data"]
        self.user_id = content["id"]

        if not self.user_id:
            raise Exception(f"No user_id in response: {content}")

        # TODO: update_account

        # TODO: get_user_privacies

        # TODO: get_minimum_jobs

        # TODO: get_columns

    @task
    def settings_modal_interaction(self):
        # update account info
        response = self.client.post(
            "/account/api/update_account",
            json.dumps(
                {
                    "id": self.user_id,
                    "first_name": self.faker.first_name(),
                    "country": self.faker.country(),
                    "field_of_work": self.faker.job(),
                }
            ),
            headers={"X-CSRFToken": self.csrftoken},
        )
        if response.status_code != 200:
            raise Exception(f"update_account error {json.loads(response.content)}")

        # TODO: update privacy options

    @task
    def kanban_job_interaction(self):
        # create job
        # get_job_by_id (50% of the time?) - to emulate non-populated jobs?
        # edit job fields
        pass

    def job_modal_request_cover_letter_review_interaction(self):
        # get_job_by_id (50% of the time?) - to emulate non-populated jobs?
        # request_review
        pass

    @task
    def kanban_column_interaction(self):
        # update columns
        pass

    @task
    def friends_modal_request_friend_interaction(self):
        # get_updated_user_data
        # search_users_by_name
        # send_friend_request
        pass

    @task
    def friends_modal_friend_request_interaction(self):
        # get_updated_user_data
        # accept_friend_request
        # deny_friend_request
        pass

    @task
    def friends_modal_friend_kanban_interaction(self):
        # get_updated_user_data
        # view_friend_kanban
        pass

    @task
    def inbox_modal_review_cover_letter_interaction(self):
        # get_updated_user_data
        # get_review_requests_for_user
        # get_reviews_for_user

        # send_review(?)
        pass
