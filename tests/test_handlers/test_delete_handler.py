from uuid import uuid4


async def test_delete_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "f_name": "Vladyslav",
        "l_name": "Yurchenko",
        "email": "lol@kek.com",
        "is_active": True,
    }
    await create_user_in_database(**user_data)
    resp = client.delete(f"/user/?user_id={user_data['user_id']}")
    assert resp.status_code == 200
    assert resp.json() == {"deleted_user_id": str(user_data["user_id"])}
    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["f_name"] == user_data["f_name"]
    assert user_from_db["l_name"] == user_data["l_name"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is False
    assert user_from_db["user_id"] == user_data["user_id"]


async def test_delete_user_not_found(client):
    user_id = uuid4()
    resp = client.delete(f"/user/?user_id={user_id}")
    assert resp.status_code == 404
    assert resp.json() == {"detail": f"User with id {user_id} not found"}


async def test_delete_user_user_id_validation_error(client):
    resp = client.delete("/user/?user_id=123")
    assert resp.status_code == 422
    data_from_response = resp.json()
    assert data_from_response == {
        'detail': [
            {
                'type': 'uuid_parsing',
                'loc': ['query', 'user_id'],
                'msg': 'Input should be a valid UUID, invalid length: expected length 32 for simple format, found 3',
                'input': '123',
                'ctx': {'error': 'invalid length: expected length 32 for simple format, found 3'},
                'url': 'https://errors.pydantic.dev/2.4/v/uuid_parsing'
            }
        ]
    }