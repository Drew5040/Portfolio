from locust import HttpUser, task, between, SequentialTaskSet
import random


class UserBehavior(SequentialTaskSet):

    @task
    def load_welcome_page(self):
        self.client.get("/")

    @task
    def wait_after_welcome(self):
        self.wait_time = between(1, 4)

    @task
    def load_about_page(self):
        self.client.get("/about")

    @task
    def wait_after_about(self):
        self.wait_time = between(1, 4)

    @task
    def load_model_page(self):
        self.client.get("/model")

    @task
    def submit_model_form(self):
        data = {
            'field1': random.choice(['Option1', 'Option2', 'Option3']),
            'field2': random.randint(10, 100),
            # Add more fields as needed
        }
        self.client.post("/model", data=data)

    @task
    def wait_after_model(self):
        self.wait_time = between(1, 10)

    @task
    def load_contact_page(self):
        self.client.get("/contact")

    @task
    def submit_contact_form(self):
        contact_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test message.'
        }
        self.client.post("/contact", data=contact_data)

    @task
    def wait_after_contact(self):
        self.wait_time = between(1, 5)

    @task
    def navigate_backwards(self):
        self.client.get("/model")
        self.client.get("/about")
        self.client.get("/")
