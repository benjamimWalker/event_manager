from app.controllers.event.event_controller import is_valid_instance_id
from app.models.model import Event
from app.utils.utils import get_random_register_from_table as get_event


def test_delete_a_event_by_id(my_client):
    mutation = {
        "query": """
            mutation($eventId: Int!) {
              deleteEventMutation(eventId: $eventId) {
                eventDeleted
              }
            }
        """
    }
    variables = {
        "eventId": get_event(Event).id
    }
    mutation['variables'] = variables

    response = my_client.post(
        url="/graphql",
        json=mutation,
        headers={
            "content_type": "application/json"
        }
    )

    assert response.status_code == 200
    assert not is_valid_instance_id(variables['eventId'], Event)


