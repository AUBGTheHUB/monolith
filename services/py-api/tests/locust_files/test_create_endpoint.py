import string
import random
from locust import HttpUser, task, between


class ApiUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def create_random_user(self) -> None:
        random_name = "test_" + "".join(random.choices(string.ascii_lowercase, k=4))
        random_email = "".join(random.choices(string.ascii_lowercase, k=4)) + "@test.com"
        team_name = "".join(random.choices(string.ascii_uppercase, k=6))
        payload = {"name": f"{random_name}", "email": f"{random_email}", "is_admin": True, "team_name": f"{team_name}"}
        print(payload, "\n")
        response = self.client.post("/hackathon/participants", json=payload)
        print(response)
