from pytest import mark


@mark.users
def test_get_all_users_query(my_client):
    query = {
        "query": '''
        {
            users{
                all{
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
    assert response.status_code == 200

    assert response.json()['data']['users']['all']

    all_users = response.json()['data']['users']['all']

    for user in range(len(all_users)):
        assert all_users[user]['name']
        assert all_users[user]['id'].isdigit()

