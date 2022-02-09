from faker import Faker

fake = Faker()

def test_create_a_new_status_instance(my_client):
    mutation = {
        "query": """
        mutation ($name: String!){
            createStatusMutation(name: $name){
                status{
                    id
                    name
                    active
                }
            }
        }
        """
    }
    variables = {
        "name": fake.sentence(nb_words=2)
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
    assert response.json()['data']['createStatusMutation']['status']['name'] == variables['name']
    assert response.json()['data']['createStatusMutation']['status']['id']
    assert response.json()['data']['createStatusMutation']['status']['id'].isdigit()

