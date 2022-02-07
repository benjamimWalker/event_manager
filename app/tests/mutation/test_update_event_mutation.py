from data.script_data import get_random_register_from_table as get_event
from app.models.model import Event
from app.db.database import session
from faker import Faker

fake = Faker()

def test_update_a_event_in_the_database(my_client):
    mutation = {
        "query": """
            mutation ($id: Int!, $description: String){
                updateEventMutation(eventData:{id:$id,description: $description}){
                event{
                    id
                    title
                    description
                    author{
                        id
                        name
                    }
                    status{
                        id
                        name
                    }
                    participants{
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
        "id": get_event(Event, session).id,
        "description": fake.sentence(nb_words=4)
    }

    mutation['variables'] = variables

    response = my_client.post(
        url="/graphql",
        json=mutation,
        headers={
            "content_type":"application/json"
        }
    )

    assert response.status_code == 200
    assert variables['id'] == int(response.json()['data']['updateEventMutation']['event']['id'])
    assert response.json()['data']['updateEventMutation']['event']['title']
    assert response.json()['data']['updateEventMutation']['event']['dateEvent']
