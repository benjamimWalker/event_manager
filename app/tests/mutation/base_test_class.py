from datetime import datetime
from faker import Faker


class BaseEventTest:
    fake = Faker()

    @staticmethod
    def get_response_data(my_client, mutation):
        return my_client.post(
            url="/graphql",
            json=mutation,
            headers={
                'content_type': 'application/json'
            }
        )