from datetime import datetime
from app.tests.mutation.base_test_class import BaseEventTest
from app.utils.utils import get_random_register_from_table as get_instance, last_data_in_the_table
from app.models.model import Event, User


class TestUpdate(BaseEventTest):
    @staticmethod
    def get_data():
        mutation = {
            "query": """
                mutation(
                      $id: Int!,
                      $participants: [Int],
                      $dateEvent: DateTime,
                      $title: String,
                      $description: String,
                      $statusId: Int
                    )
                    {
                        updateEventMutation(
                            dataEvent: {
                                id: $id,
                                title: $title,
                                description: $description,
                                participants: $participants,
                                dateEvent: $dateEvent,
                                statusId: $statusId
                        }) {
                        event {
                            id
                            title
                            description
                            status {
                                id
                                name
                            }
                            participants {
                                id
                                name
                            }
                            dateCreated
                            dateEvent
                            }
                        }
                    }
            """
        }

        variables = {
            "id": get_instance(Event).id,
            "title": TestUpdate.fake.sentence(nb_words=5),
            "description": TestUpdate.fake.sentence(nb_words=10),
            "dateEvent": f"{'T'.join(str(datetime.now()).split())}",
            "participants": [get_instance(User).id for n in range(1, 4)]
        }

        mutation['variables'] = variables

        return mutation

    def test_update_event(self, my_client):
        mutation = TestUpdate.get_data()

        response = TestUpdate.get_response_data(my_client, mutation)

        assert response.status_code == 200
        assert mutation['variables']['id'] == int(response.json()['data']['updateEventMutation']['event']['id'])
        assert response.json()['data']['updateEventMutation']['event']['title'] == mutation['variables']['title']
        assert response.json()['data']['updateEventMutation']['event']['dateEvent'] == mutation['variables']['dateEvent']
        assert response.json()['data']['updateEventMutation']['event']['description'] == mutation['variables']['description']
        for user in response.json()['data']['updateEventMutation']['event']['participants']:
            assert int(user['id']) in mutation['variables']['participants']

    def test_update_title_to_none(self, my_client):
        mutation = TestUpdate.get_data()
        mutation['variables']['title'] = None

        response = TestUpdate.get_response_data(my_client, mutation)

        assert response.status_code == 200

        assert mutation['variables']['id'] == int(response.json()['data']['updateEventMutation']['event']['id'])
        assert response.json()['data']['updateEventMutation']['event']['title'] != mutation['variables']['title']
        assert response.json()['data']['updateEventMutation']['event']['description'] == mutation['variables']['description']

    def test_update_participants(self, my_client):
        mutation = TestUpdate.get_data()
        last_user_id = last_data_in_the_table(User)
        mutation['variables']['participants'] = [i for i in range(last_user_id + 1, last_user_id + 4)]

        response = TestUpdate.get_response_data(my_client, mutation)

        assert response.status_code == 400
        assert response.json()['errors'][0]['message'].endswith(' não é válido.')

    def test_update_description_to_none(self, my_client):
        mutation = TestUpdate.get_data()
        mutation['variables']['description'] = None

        response = TestUpdate.get_response_data(my_client, mutation)

        assert response.status_code == 200
        assert mutation['variables']['id'] == int(response.json()['data']['updateEventMutation']['event']['id'])
        assert response.json()['data']['updateEventMutation']['event']['description'] != mutation['variables']['description']
        assert response.json()['data']['updateEventMutation']['event']['title'] == mutation['variables']['title']

