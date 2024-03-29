import django
from dotenv import load_dotenv
from locust import HttpUser, task, between
from faker import Faker
import json
from django.utils import timezone

# Required to setup django, allowing for module import(s) below
load_dotenv()
django.setup()

from account.models import User, FriendRequest  # noqa: E402


class UserActor(HttpUser):
    wait_time = between(10, 12)

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
            raise ValueError(f"get_or_create_account error {response.content}")

        content = json.loads(response.content)
        self.user_id = content["data"]["id"]
        self.token = content["token"]

        self.client.cookies.set("auth_token", self.token)

        if not self.user_id:
            raise ValueError(f"No user_id in response: {content}")

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
            raise ValueError(f"update_account error {response.content}")

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
            raise ValueError(f"get_user_privacies error {response.content}")

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
            raise ValueError(f"get_minimum_jobs error {response.content}")

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
            raise ValueError(f"No columns in response: {content}")

        if response.status_code != 200:
            raise ValueError(f"get_columns error {content}")

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
            raise ValueError(f"update_account error {response.content}")

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
            raise ValueError(f"update_privacies error {response.content}")

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
            raise ValueError(f"create_job error {response.content}")

        content = json.loads(response.content)
        job_id = content["job"]["id"]

        if not job_id:
            raise ValueError("No job id returned from create_job")

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
                raise ValueError(f"get_job_by_id error {response.content}")

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
            raise ValueError(f"update_job error {response.content}")

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
            raise ValueError(f"create_job error {response.content}")

        content = json.loads(response.content)
        job_id = content["job"]["id"]

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
                raise ValueError(f"get_job_by_id error {response.content}")

        # Create Account, Add Friends
        response = self.client.post(
            "/account/api/get_or_create_account",
            json.dumps({"credential": "load_test", "client_id": "load_test"}),
            headers={"X-CSRFToken": self.csrftoken},
        )
        if response.status_code != 200:
            raise ValueError(f"get_or_create_account error {response.content}")

        content = json.loads(response.content)
        user_id = content["data"]["id"]

        User.objects.get(id=self.user_id).friends.set([User.objects.get(id=user_id)])

        # Send review request
        response = self.client.post(
            "/job/api/create_review_request",
            json.dumps({"job_id": job_id, "reviewer_id": user_id, "message": "Review Please"}),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise ValueError(f"create_review_request error {response.content}")

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
            raise ValueError(f"update_columns error {response.content}")

    @task
    def friends_modal_request_friend_interaction(self):
        # get updated user data
        response = self.client.post(
            "/account/api/get_updated_user_data",
            json.dumps(self.token),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise ValueError(f"get_updated_user_data error {response.content}")

        # search_users_by_name
        response = self.client.post(
            "/account/api/search_users_by_name",
            json.dumps("j"),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise ValueError(f"search_users_by_name error {response.content}")

        # Create Account To Send Request To
        response = self.client.post(
            "/account/api/get_or_create_account",
            json.dumps({"credential": "load_test", "client_id": "load_test"}),
            headers={"X-CSRFToken": self.csrftoken},
        )
        if response.status_code != 200:
            raise ValueError(f"get_or_create_account error {response.content}")

        content = json.loads(response.content)
        user_id = content["data"]["id"]

        # send friend request
        response = self.client.post(
            "/account/api/create_friend_request",
            json.dumps({"from_user_id": self.user_id, "to_user_id": user_id}),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise ValueError(f"create_friend_request error {response.content}")

    @task
    def friends_modal_friend_request_interaction(self):
        # get updated user data
        response = self.client.post(
            "/account/api/get_updated_user_data",
            json.dumps(self.token),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise ValueError(f"get_updated_user_data error {response.content}")

        # create user
        response = self.client.post(
            "/account/api/get_or_create_account",
            json.dumps({"credential": "load_test", "client_id": "load_test"}),
            headers={"X-CSRFToken": self.csrftoken},
        )
        if response.status_code != 200:
            raise ValueError(f"get_or_create_account error {response.content}")

        content = json.loads(response.content)
        user_id = content["data"]["id"]

        # update self privacy to be searchable
        response = self.client.post(
            "/account/api/update_privacies",
            json.dumps(
                {
                    "user_id": self.user_id,
                    "privacies": {
                        "is_searchable": True,
                        "share_kanban": self.faker.boolean(),
                        "cover_letter_requestable": self.faker.boolean(),
                    },
                }
            ),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise ValueError(f"update_privacies error {response.content}")

        # make object manually to avoid endpoint validation
        FriendRequest.objects.create(
            from_user=User.objects.get(id=user_id),
            to_user=User.objects.get(id=self.user_id),
            sent=timezone.now(),
            accepted=False,
            acknowledged=None,
        )

        if response.status_code != 200:
            raise ValueError(f"create_friend_request error {response.content}")

        # get updated user data
        response = self.client.post(
            "/account/api/get_updated_user_data",
            json.dumps(self.token),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise ValueError(f"get_updated_user_data error {response.content}")

        received_requests = json.loads(response.content)["user"]["received_friend_requests"]

        # ~50/50 accept/deny request
        if self.faker.boolean():
            response = self.client.post(
                "/account/api/accept_friend_request",
                json.dumps(
                    {"request_id": received_requests[0]["id"], "from_user_id": user_id, "to_user_id": self.user_id}
                ),
                headers={"X-CSRFToken": self.csrftoken},
            )

            if response.status_code != 200:
                raise ValueError(f"deny_friend_request error {response.content}")
        else:
            response = self.client.post(
                "/account/api/deny_friend_request",
                json.dumps(
                    {"request_id": received_requests[0]["id"], "from_user_id": user_id, "to_user_id": self.user_id}
                ),
                headers={"X-CSRFToken": self.csrftoken},
            )

            if response.status_code != 200:
                raise ValueError(f"deny_friend_request error {response.content}")

    @task
    def friends_modal_friend_kanban_interaction(self):
        # get updated user data
        response = self.client.post(
            "/account/api/get_updated_user_data",
            json.dumps(self.token),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise ValueError(f"get_updated_user_data error {response.content}")

        # create new user, add friends
        response = self.client.post(
            "/account/api/get_or_create_account",
            json.dumps({"credential": "load_test", "client_id": "load_test"}),
            headers={"X-CSRFToken": self.csrftoken},
        )
        if response.status_code != 200:
            raise ValueError(f"get_or_create_account error {response.content}")

        content = json.loads(response.content)
        user_id = content["data"]["id"]

        User.objects.get(id=self.user_id).friends.set([User.objects.get(id=user_id)])

        # view friend kanban
        response = self.client.post(
            "/account/api/get_friend_data",
            json.dumps({"user_id": self.user_id, "friend_id": user_id}),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise ValueError(f"get_friend_data error {response.content}")

    @task
    def inbox_modal_review_cover_letter_interaction(self):
        # get updated user data
        response = self.client.post(
            "/account/api/get_updated_user_data",
            json.dumps(self.token),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise ValueError(f"get_updated_user_data error {response.content}")

        # get review requests
        response = self.client.post(
            "/job/api/get_review_requests_for_user",
            json.dumps({"user_id": self.user_id}),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise ValueError(f"get_review_requests_for_user error {response.content}")

        # get reviews for user
        response = self.client.post(
            "/job/api/get_reviews_for_user",
            json.dumps({"user_id": self.user_id}),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise ValueError(f"get_reviews_for_user error {response.content}")

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
            raise ValueError(f"create_job error {response.content}")

        content = json.loads(response.content)
        job_id = content["job"]["id"]

        # create user
        response = self.client.post(
            "/account/api/get_or_create_account",
            json.dumps({"credential": "load_test", "client_id": "load_test"}),
            headers={"X-CSRFToken": self.csrftoken},
        )
        if response.status_code != 200:
            raise ValueError(f"get_or_create_account error {response.content}")

        content = json.loads(response.content)
        user_id = content["data"]["id"]

        # add friend
        User.objects.get(id=self.user_id).friends.set([User.objects.get(id=user_id)])

        # create review request
        response = self.client.post(
            "/job/api/create_review_request",
            json.dumps({"job_id": job_id, "reviewer_id": user_id, "message": "Review Please"}),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise ValueError(f"create_review_request error {response.content}")

        request_id = json.loads(response.content)["review_request"]["id"]

        # send review
        response = self.client.post(
            "/job/api/create_review",
            json.dumps({"request_id": request_id, "response": "Review Response"}),
            headers={"X-CSRFToken": self.csrftoken},
        )

        if response.status_code != 200:
            raise ValueError(f"create_review error {response.content}")
