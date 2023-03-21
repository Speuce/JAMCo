from locust import HttpUser, task, between
from faker import Faker
import json


class UserActor(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.faker = Faker()

        response = self.client.get("/")
        self.csrftoken = response.cookies["csrftoken"]

        # tasks require self.user_id to be set
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

    @task(1)
    def update_account(self):
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
