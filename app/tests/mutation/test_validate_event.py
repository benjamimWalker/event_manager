from datetime import datetime

from faker import Faker
from app.models.model import User, Status
from app.utils.utils import is_valid_instance_id, last_data_in_the_table
from .base_test_class import BaseEventTest
from typing import Dict
from app.utils.utils import get_random_register_from_table as get_instance
from app.models.model import User, Status


class TestValidated(BaseEventTest):
    @staticmethod
    def get_mutation_data() -> Dict:
        mutation = {
            "query": """
                     mutation (
                            $authorId: Int!,
                            $statusId: Int!,
                            $participants: [Int]!,
                            $dateEvent: DateTime!,
                            $title: String!,
                            $description: String!
                        ) {
                        createEventMutation(dataEvent: {
                                title: $title
                                description: $description
                                authorId: $authorId
                                statusId: $statusId
                                participants: $participants
                                dateEvent: $dateEvent
                            }) {
                            event {
                                id
                                title
                                dateEvent
                                author {
                                    id
                                    name
                                }
                                participants {
                                    id
                                    name
                                }
                                status{
                                    id
                                    name
                                }
                            }
                        }
                    }
                    """
        }

        variables = {
            "title": BaseEventTest.fake.sentence(nb_words=5),

            "description": BaseEventTest.fake.sentence(nb_words=10),

            "dateEvent": f"{'T'.join(str(datetime.now()).split())}",

            "authorId": get_instance(User).id,

            "statusId": get_instance(Status).id,

            "participants": [get_instance(User).id for n in range(1, 4)]
        }

        mutation['variables'] = variables

        return mutation

    def test_create_event(self, my_client):
        mutation = TestValidated.get_mutation_data()
        response = TestValidated.get_response_data(my_client, mutation)

        assert response.status_code == 200
        assert mutation['variables']['title'] == response.json()['data']['createEventMutation']['event']['title']
        assert response.json()['data']['createEventMutation']['event']['id'].isdigit()
        assert response.json()['data']['createEventMutation']['event']['status']['id'].isdigit()
        assert len(response.json()['data']['createEventMutation']['event']['participants']) > 0
        assert len(response.json()['data']['createEventMutation']['event']['title']) > 5
        assert is_valid_instance_id(int(response.json()['data']['createEventMutation']['event']["status"]['id']),
                                    Status)

    def test_validate_title(self, my_client):
        mutation = TestValidated.get_mutation_data()
        mutation['variables']['title'] = TestValidated.fake.sentence(nb_words=1)[:3]

        response = TestValidated.get_response_data(my_client, mutation)

        assert response.status_code == 400
        assert response.json()['errors'][0]['message']
        assert response.json()['errors'][0]['message'] == "Informe um titulo válido."

    def test_validate_description(self, my_client):
        mutation = TestValidated.get_mutation_data()
        mutation['variables']['description'] = TestValidated.fake.sentence(nb_words=1)[:5]

        response = TestValidated.get_response_data(my_client, mutation)

        assert response.status_code == 400
        assert response.json()['errors'][0]['message']
        assert response.json()['errors'][0]['message'] == "Informe uma descrição válida."

    def test_validate_author_id(self, my_client):
        mutation = TestValidated.get_mutation_data()
        mutation['variables']['authorId'] = None

        response = TestValidated.get_response_data(my_client, mutation)

        assert response.status_code == 400
        assert response.json()['errors']
        assert response.json()['errors'][0]['message']

    def test_validate_status_id(self, my_client):
        mutation = TestValidated.get_mutation_data()
        mutation['variables']['statusId'] = None

        response = TestValidated.get_response_data(my_client, mutation)

        assert response.status_code == 400
        assert response.json()['errors'][0]['message']

        mutation['variables']['statusId'] = last_data_in_the_table(Status) + 1

        response = TestValidated.get_response_data(my_client, mutation)

        assert response.status_code == 400
        assert response.json()['errors'][0]['message'] == "Informe um status válido."

    def test_validate_participants(self, my_client):
        mutation = TestValidated.get_mutation_data()
        last_user_id = last_data_in_the_table(User)
        mutation['variables']['participants'] = [i for i in range(last_user_id+1, last_user_id+4)]

        response = TestValidated.get_response_data(my_client, mutation)

        assert response.status_code == 400
        assert response.json()['errors'][0]['message'].endswith(' não é válido.')

