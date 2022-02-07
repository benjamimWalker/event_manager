import datetime
from app.models.model import User, Status
from data.script_data import get_random_register_from_table as get_user
from data.script_data import get_random_register_from_table as get_status
from app.db.database import session
from faker import Faker

fake = Faker()


def test_create_a_new_event(my_client):
    mutation = {
        "query": """
            mutation (
                $authorId: Int!,
                $statusId: Int,
                $participants: [Int]!,
                $dateEvent: DateTime,
                $title: String!,
                $description: String!
            ) {
            createEventMutation(
                eventData: {
                    title: $title
                    description: $description
                    authorId: $authorId
                    statusId: $statusId
                    participants: $participants
                    dateEvent: $dateEvent
                    active: true
                }
                ) {
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
        "title": fake.sentence(nb_words=4),

        "description":  fake.sentence(nb_words=10),

        "dateEvent": f"{'T'.join(str(datetime.datetime.now()).split())}",

        "authorId": get_user(User, session).id,

        "statusId": get_status(Status, session).id,

        "participants": [get_user(User, session).id for n in range(3)]
    }

    mutation["variables"] = variables

    response = my_client.post(
        url="/graphql",
        json=mutation,
        headers={
            "content_type": "application/json"
        }
    )

    assert response.status_code == 200
    assert variables['title'] == response.json()['data']['createEventMutation']['event']['title']
    assert response.json()['data']['createEventMutation']['event']['id'].isdigit()
    assert response.json()['data']['createEventMutation']['event']['status']['id'].isdigit()
    assert response.json()['data']['createEventMutation']['event']['participants']

