from faker import Faker

fake = Faker()

def test_create_a_new_user(my_client):
    mutation = {
        'query': '''
            mutation ($name: String!){
                createUserMutation(userData: { name: $name, active: true }) {
                    user {
                        id
                        name
                        active
                    }
                }
            }
        '''
    }

    variables = {
        "name": fake.name()
    }

    mutation['variables'] = variables

    response = my_client.post(
        url='/graphql',
        json=mutation,
        headers={
            'content_type': 'application/json'
        }
    )

    assert response.status_code == 200
    assert variables['name'] == response.json()['data']['createUserMutation']['user']['name']
    assert response.json()['data']['createUserMutation']['user']['active']
    assert response.json()['data']['createUserMutation']['user']['id'].isdigit()

