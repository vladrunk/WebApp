import json
from uuid import uuid4

import pytest


async def test_update_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "f_name": "Vladyslav",
        "l_name": "Yurchenko",
        "email": "lol@kek.com",
        "is_active": True,
    }
    user_data_updated = {
        "f_name": "Vladrunk",
        "l_name": "Enot",
        "email": "cheburek@kek.com",
    }
    await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data['user_id']}", data=json.dumps(user_data_updated)
    )
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["updated_user_id"] == str(user_data["user_id"])
    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["f_name"] == user_data_updated["f_name"]
    assert user_from_db["l_name"] == user_data_updated["l_name"]
    assert user_from_db["email"] == user_data_updated["email"]
    assert user_from_db["is_active"] is user_data["is_active"]
    assert user_from_db["user_id"] == user_data["user_id"]


async def test_update_user_check_one_is_updated(
        client, create_user_in_database, get_user_from_database
):
    user_data_1 = {
        "user_id": uuid4(),
        "f_name": "Vladyslav",
        "l_name": "Yurchenko",
        "email": "lol@kek.com",
        "is_active": True,
    }
    user_data_2 = {
        "user_id": uuid4(),
        "f_name": "Ivan",
        "l_name": "Ivanov",
        "email": "ivan@kek.com",
        "is_active": True,
    }
    user_data_3 = {
        "user_id": uuid4(),
        "f_name": "Petr",
        "l_name": "Petrov",
        "email": "petr@kek.com",
        "is_active": True,
    }
    user_data_updated = {
        "f_name": "Yur",
        "l_name": "Yurchov",
        "email": "cheburek@kek.com",
    }
    for user_data in [user_data_1, user_data_2, user_data_3]:
        await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data_1['user_id']}", data=json.dumps(user_data_updated)
    )
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["updated_user_id"] == str(user_data_1["user_id"])
    users_from_db = await get_user_from_database(user_data_1["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["f_name"] == user_data_updated["f_name"]
    assert user_from_db["l_name"] == user_data_updated["l_name"]
    assert user_from_db["email"] == user_data_updated["email"]
    assert user_from_db["is_active"] is user_data_1["is_active"]
    assert user_from_db["user_id"] == user_data_1["user_id"]

    # check other users that data has not been changed
    users_from_db = await get_user_from_database(user_data_2["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["f_name"] == user_data_2["f_name"]
    assert user_from_db["l_name"] == user_data_2["l_name"]
    assert user_from_db["email"] == user_data_2["email"]
    assert user_from_db["is_active"] is user_data_2["is_active"]
    assert user_from_db["user_id"] == user_data_2["user_id"]

    users_from_db = await get_user_from_database(user_data_3["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["f_name"] == user_data_3["f_name"]
    assert user_from_db["l_name"] == user_data_3["l_name"]
    assert user_from_db["email"] == user_data_3["email"]
    assert user_from_db["is_active"] is user_data_3["is_active"]
    assert user_from_db["user_id"] == user_data_3["user_id"]


@pytest.mark.parametrize(
    "user_data_updated, expected_status_code, expected_detail",
    [
        (
            {},
            422,
            {"detail": 'At least one parameter for user update info should be provided'},
        ),
        (
            {"f_name": "123"},
            422,
            {"detail": "First name should contains only letters"}
        ),
        (
            {"email": ""},
            422,
            {
                'detail': [
                    {
                        'ctx': {'reason': 'The email address is not valid. It must have exactly one @-sign.'},
                        'input': '',
                        'loc': ['body', 'email'],
                        'msg': 'value is not a valid email address: The email address is not valid. It must have '
                               'exactly one @-sign.',
                        'type': 'value_error'
                    }
                ]
            }
        ),
        (
            {"l_name": ""},
            422,
            {
                'detail': [
                    {
                        'ctx': {'min_length': 1},
                        'input': '',
                        'loc': ['body', 'l_name'],
                        'msg': 'String should have at least 1 characters',
                        'type': 'string_too_short',
                        'url': 'https://errors.pydantic.dev/2.4/v/string_too_short'
                    }
                ]
            }
        ),
        (
            {"f_name": ""},
            422,
            {
                'detail': [
                    {
                        'ctx': {'min_length': 1},
                        'input': '',
                        'loc': ['body', 'f_name'],
                        'msg': 'String should have at least 1 characters',
                        'type': 'string_too_short',
                        'url': 'https://errors.pydantic.dev/2.4/v/string_too_short'
                    }
                ]
            }
        ),
        (
            {"l_name": "123"},
            422,
            {"detail": "Last name should contains only letters"}),
        (
            {"email": "123"},
            422,
            {
                'detail': [
                    {
                        'ctx': {'reason': 'The email address is not valid. It must have exactly one @-sign.'},
                        'input': '123',
                        'loc': ['body', 'email'],
                        'msg': 'value is not a valid email address: The email address is not valid. It must have '
                               'exactly one @-sign.',
                        'type': 'value_error'
                    }
                ]
            }
        ),
    ],
)
async def test_update_user_validation_error(client, create_user_in_database, get_user_from_database, user_data_updated,
                                            expected_status_code, expected_detail):
    user_data = {
        "user_id": uuid4(),
        "f_name": "Vladyslav",
        "l_name": "Yurchenko",
        "email": "lol@kek.com",
        "is_active": True,
    }
    await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data['user_id']}", data=json.dumps(user_data_updated)
    )
    assert resp.status_code == expected_status_code
    resp_data = resp.json()
    assert resp_data == expected_detail


async def test_update_user_id_validation_error(client):
    user_data_updated = {
        "f_name": "Ivan",
        "l_name": "Ivanov",
        "email": "cheburek@kek.com",
    }
    resp = client.patch("/user/?user_id=123", data=json.dumps(user_data_updated))
    assert resp.status_code == 422
    data_from_response = resp.json()
    assert data_from_response == {
        'detail': [
            {
                'ctx': {'error': 'invalid length: expected length 32 for simple format, found 3'},
                'input': '123',
                'loc': ['query', 'user_id'],
                'msg': 'Input should be a valid UUID, invalid length: expected length 32 for simple format, found 3',
                'type': 'uuid_parsing',
                'url': 'https://errors.pydantic.dev/2.4/v/uuid_parsing'
            }
        ]
    }


async def test_update_user_not_found_error(client):
    user_data_updated = {
        "f_name": "Ivan",
        "l_name": "Ivanov",
        "email": "cheburek@kek.com",
    }
    user_id = uuid4()
    resp = client.patch(f"/user/?user_id={user_id}", data=json.dumps(user_data_updated))
    assert resp.status_code == 404
    resp_data = resp.json()
    assert resp_data == {"detail": f"User with id {user_id} not found"}


async def test_update_user_duplicate_email_error(client, create_user_in_database):
    user_data_1 = {
        "user_id": uuid4(),
        "f_name": "Vladyslav",
        "l_name": "Yurchenko",
        "email": "lol@kek.com",
        "is_active": True,
    }
    user_data_2 = {
        "user_id": uuid4(),
        "f_name": "Ivan",
        "l_name": "Ivanov",
        "email": "ivan@kek.com",
        "is_active": True,
    }
    user_data_updated = {
        "email": user_data_2["email"],
    }
    for user_data in [user_data_1, user_data_2]:
        await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data_1['user_id']}", data=json.dumps(user_data_updated)
    )
    assert resp.status_code == 503
    assert 'duplicate key value violates unique constraint "users_email_key"' in resp.json()["detail"]
