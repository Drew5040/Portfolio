from random import choice, randint
from locust import HttpUser, between, SequentialTaskSet, task, run_single_user, events
from locust.exception import StopUser


class UserBehavior(SequentialTaskSet):
    wait_time = between(10, 20)

    @task
    def load_welcome_page(self):
        self.client.get("/")

    @task
    def load_about_page(self):
        self.client.get("/about")

    @task
    def load_model_page(self):
        self.client.get("/model")

    @task
    def submit_model_form(self):
        data = {

            'w_class': choice(['0', '1', '2', '3', '4', '5', '6', '7']),
            'edu': choice([str(i) for i in range(16)]),
            'marital_stat': choice(['0', '1', '2']),
            'occupation': choice([str(i) for i in range(14)]),
            'relation': choice(['0', '1', '2', '3', '4', '5']),
            'race': choice(['0', '1', '2', '3', '4']),
            'gender': choice(['0', '1']),
            'c_gain': str(randint(0, 99999)),
            'c_loss': str(randint(0, 4356)),
            'hours_per_week': str(randint(1, 99)),
            'native-country': choice([str(i) for i in range(41)])
        }
        self.client.post("/model", data=data)

    @task
    def load_contact_page(self):
        self.client.get("/contact")

    @task
    def submit_contact_form(self):
        contact_data = {

            'email': 'andrewodrain@outlook.com',
            'name': 'Ziggy User',
            'subject': 'Free Boobers For All',
            'message': 'This is a test message.'
        }
        self.client.post("/contact", data=contact_data)

    @task
    def navigate_backwards(self):
        self.client.get("/model")
        self.client.get("/about")
        self.client.get("/")

    @task
    def navigate_forwards(self):
        self.client.get("/about")
        self.client.get("/model")
        self.client.get("/contact")


class AppUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)

    # @task
    # def contact_form_error(self):
    #     response = self.client.post("/contact", data={"key": "value"})
    #     if response.status_code == 500:
    #         events.request_failure.fire(
    #
    #             request_type="POST",
    #             name="/contact",
    #             response_time=response.elapsed.total_seconds(),
    #             exception=None,
    #             response=response
    #
    #         )
    #     raise StopUser("Encountered 500 error. Stopping test.")
    #
    # def on_stop(self):
    #     pass


if __name__ == '__main__':
    run_single_user(AppUser)
