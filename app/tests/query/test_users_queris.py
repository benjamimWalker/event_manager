from pytest import mark


@mark.users
def test_get_all_users_query(my_client):
    query = {
        "query": '''
        {
            users{
                items{
                    id
                    name
                }
            }
        }
    '''}

    response = my_client.post(
        url='/graphql',
        json=query,
        headers={
            'content_type': 'application/json'
        }
    )

    all_users = response.json()['data']['users']['items']

    number_of_users = len(all_users)

    number_of_valid_users = len([user['id'] for user in all_users if user['id']])

    assert response.status_code == 200
    assert number_of_users != 0
    assert number_of_valid_users == number_of_users

