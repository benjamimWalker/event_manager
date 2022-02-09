from pytest import mark
from app.utils.utils import get_random_register_from_table as get_event
from app.models.model import Event


@mark.events
def test_get_events_from_event_table(my_client):
    query = {
        'query': """
            {
                events {
                    all {
                        id
                        title
                        dateEvent
                        description
                        author{
                            id
                            name
                        }
                        participants{
                            id
                            name
                        }
                    }
                }
            }
        """
    }

    response = my_client.post(
        url="/graphql",
        json=query,
        headers={
            "content_type": "application/json"
        }
    )

    all_events = response.json()['data']['events']['all']

    assert response.status_code == 200

    assert all_events

    for instance in range(len(all_events)):
        for participant in range(len(all_events[instance]['participants'])):
            assert all_events[instance]['participants'][participant]['name']
            assert all_events[instance]['participants'][participant]['id'].isdigit()
        assert all_events[instance]['title']
        assert all_events[instance]['author']['name']
        assert all_events[instance]['author']['id'].isdigit()


@mark.event
def test_get_one_event_from_events_table(my_client):
    query = {
        "query": """
        query ($id:Int!){
            events{
                item(eventId: $id){
                    id
                    title
                    description
                    dateEvent
                    status{
                        id
                        name
                    }
                    author{
                        id
                        name
                    }
                    participants{
                        id
                        name
                    }
                }
            }
        }
        """
    }
    variables = {
        "id": get_event(Event).id
    }

    query['variables'] = variables

    response = my_client.post(
        url="/graphql",
        json=query,
        headers={
            "content_type": "application/json"
        }
    )

    assert response.status_code
    assert variables['id'] == int(response.json()['data']['events']['item']['id'])
    assert response.json()['data']['events']['item']
    assert response.json()['data']['events']['item']['id'].isdigit()
    assert response.json()['data']['events']['item']['author']['id']
    assert response.json()['data']['events']['item']['participants']
