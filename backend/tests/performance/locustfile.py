import django
from dotenv import load_dotenv
from locust import HttpUser, task, between
from faker import Faker
import json

# Required to setup django, allowing for module import(s) below
load_dotenv()
django.setup()

from account.models import User  # noqa: E402


# TODO: Create Test DB On Locust Launch - TestCase?
class UserActor(HttpUser):
    wait_time = between(0, 1)  # 5, 10

    # __init__ not required for locust
    # Only used to define object fields accessed in @tasks
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = None
        self.token = None
        self.columns = None

    def on_start(self):
        self.login()

    # simulate login, called first
    def login(self):
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
            raise Exception(f"get_or_create_account error {response.content}")

        content = json.loads(response.content)
        self.user_id = content["data"]["id"]
        self.token = content["token"]

        if not self.user_id:
            raise Exception(f"No user_id in response: {content}")

        # update account fields
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
            raise Exception(f"update_account error {response.content}")

        # get user privacies
        response = self.client.post(
            "/account/api/get_user_privacies",
            json.dumps(
                {
                    "user_id": self.user_id,
                }
            ),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise Exception(f"get_user_privacies error {response.content}")

        # TODO: Create jobs for get_minimum_jobs to return?

        # get minimum jobs
        response = self.client.post(
            "/job/api/get_minimum_jobs",
            json.dumps(
                {
                    "user_id": self.user_id,
                }
            ),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise Exception(f"get_minimum_jobs error {response.content}")

        # get user's columns
        response = self.client.post(
            "/column/api/get_columns",
            json.dumps(
                {
                    "user_id": self.user_id,
                }
            ),
            headers={"X-CSRFToken": self.csrftoken},
        )

        content = json.loads(response.content)

        self.columns = content["columns"]

        if not self.columns:
            raise Exception(f"No columns in response: {content}")

        if response.status_code != 200:
            raise Exception(f"get_columns error {content}")

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
            raise Exception(f"update_account error {response.content}")

        # update user privacy options
        response = self.client.post(
            "/account/api/update_privacies",
            json.dumps(
                {
                    "user_id": self.user_id,
                    "privacies": {
                        "is_searchable": self.faker.boolean(),
                        "share_kanban": self.faker.boolean(),
                        "cover_letter_requestable": self.faker.boolean(),
                    },
                }
            ),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise Exception(f"update_privacies error {response.content}")

    @task
    def kanban_job_interaction(self):
        # create job
        response = self.client.post(
            "/job/api/create_job",
            json.dumps(
                {
                    "user_id": self.user_id,
                    "position_title": self.faker.job(),
                    "company": self.faker.company(),
                    "type": self.faker.safe_color_name(),
                    "kcolumn_id": self.columns[0]["id"],
                }
            ),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise Exception(f"create_job error {response.content}")

        content = json.loads(response.content)
        job_id = content["job"]["id"]

        if not job_id:
            raise Exception("No job id returned from create_job")

        # ~50% of the time in order to emulate non-populated kanban job
        if self.faker.boolean():
            # get job by id
            response = self.client.post(
                "/job/api/get_job_by_id",
                json.dumps(
                    {
                        "user_id": self.user_id,
                        "job_id": job_id,
                    }
                ),
                headers={"X-CSRFToken": self.csrftoken},
            )

            if response.status_code != 200:
                raise Exception(f"get_job_by_id error {response.content}")

        # edit job fields
        response = self.client.post(
            "/job/api/update_job",
            json.dumps(
                {
                    "user_id": self.user_id,
                    "id": job_id,
                    "position_title": self.faker.job(),
                    "company": self.faker.company(),
                    "type": self.faker.safe_color_name(),
                }
            ),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise Exception(f"update_job error {response.content}")

    @task
    def job_modal_request_cover_letter_review_interaction(self):
        # create job
        response = self.client.post(
            "/job/api/create_job",
            json.dumps(
                {
                    "user_id": self.user_id,
                    "position_title": self.faker.job(),
                    "company": self.faker.company(),
                    "type": self.faker.safe_color_name(),
                    "kcolumn_id": self.columns[0]["id"],
                }
            ),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise Exception(f"create_job error {response.content}")

        new_job_id = json.loads(response.content)["job"]["id"]

        # ~50% of the time in order to emulate non-populated kanban job
        if self.faker.boolean():
            # get job by id
            response = self.client.post(
                "/job/api/get_job_by_id",
                json.dumps(
                    {
                        "user_id": self.user_id,
                        "job_id": new_job_id,
                    }
                ),
                headers={"X-CSRFToken": self.csrftoken},
            )

            if response.status_code != 200:
                raise Exception(f"get_job_by_id error {response.content}")

        # Create Account, Add Friends
        response = self.client.post(
            "/account/api/get_or_create_account",
            json.dumps({"credential": "load_test", "client_id": "load_test"}),
            headers={"X-CSRFToken": self.csrftoken},
        )
        if response.status_code != 200:
            raise Exception(f"get_or_create_account error {response.content}")

        friend_user_id = json.loads(response.content)["data"]["id"]
        User.objects.get(id=self.user_id).friends.set([User.objects.get(id=friend_user_id)])

        # Send review request
        response = self.client.post(
            "/job/api/create_review_request",
            json.dumps({"job_id": new_job_id, "reviewer_id": friend_user_id, "message": "Review Please"}),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise Exception(f"create_review_request error {response.content}")

    @task
    def kanban_column_interaction(self):
        # update columns
        response = self.client.post(
            "/column/api/update_columns",
            json.dumps(
                {
                    "user_id": self.user_id,
                    "payload": [
                        {"id": self.columns[0]["id"], "name": self.faker.safe_color_name(), "column_number": 3},
                        {"id": self.columns[1]["id"], "name": self.faker.safe_color_name(), "column_number": 2},
                        {"id": self.columns[2]["id"], "name": self.faker.safe_color_name(), "column_number": 1},
                        {"id": self.columns[3]["id"], "name": self.faker.safe_color_name(), "column_number": 0},
                    ],
                }
            ),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise Exception(f"update_columns error {response.content}")

    @task
    def friends_modal_request_friend_interaction(self):
        # get updated user data
        response = self.client.post(
            "/account/api/get_updated_user_data",
            json.dumps(self.token),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise Exception(f"get_updated_user_data error {response.content}")

        # TODO: search_users_by_name
        # TODO: send_friend_request

    @task
    def friends_modal_friend_request_interaction(self):
        # get updated user data
        response = self.client.post(
            "/account/api/get_updated_user_data",
            json.dumps(self.token),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise Exception(f"get_updated_user_data error {response.content}")

        # TODO: accept_friend_request
        # and/or
        # TODO: deny_friend_request

    @task
    def friends_modal_friend_kanban_interaction(self):
        # get updated user data
        response = self.client.post(
            "/account/api/get_updated_user_data",
            json.dumps(self.token),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise Exception(f"get_updated_user_data error {response.content}")

        # TODO: view_friend_kanban

    @task
    def inbox_modal_review_cover_letter_interaction(self):
        # get updated user data
        response = self.client.post(
            "/account/api/get_updated_user_data",
            json.dumps(self.token),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise Exception(f"get_updated_user_data error {response.content}")

        # TODO: get_review_requests_for_user
        # TODO: get_reviews_for_user

        # TODO: send_review(?)
