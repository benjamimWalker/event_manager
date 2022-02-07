from pytest import mark


@mark.status
def test_get_all_statuses_query(my_client):
    query = {
        "query": """
            {
                statuses{
                    items{
                        id
                        name
                        active
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
    all_statuses = response.json()['data']['statuses']['items']

    assert response.status_code

    assert len(all_statuses) > 0

    for instance in range(len(all_statuses)):
        assert all_statuses[instance]['name']
        assert int(all_statuses[instance]['id']) > 0

