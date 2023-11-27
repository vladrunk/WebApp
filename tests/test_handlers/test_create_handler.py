import json

import pytest


async def test_create_user(client, get_user_from_database):
    user_data = {"f_name": "Vladyslav", "l_name": "Yurchenko", "email": "lol@kek.com"}
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["f_name"] == user_data["f_name"]
    assert data_from_resp["l_name"] == user_data["l_name"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["f_name"] == user_data["f_name"]
    assert user_from_db["l_name"] == user_data["l_name"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]


async def test_create_user_duplicate_email_error(client, get_user_from_database):
    user_data = {"f_name": "Vladyslav", "l_name": "Yurchenko", "email": "lol@kek.com"}
    user_data_same_email = {"f_name": "Petr", "l_name": "Petrov", "email": "lol@kek.com"}
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["f_name"] == user_data["f_name"]
    assert data_from_resp["l_name"] == user_data["l_name"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["f_name"] == user_data["f_name"]
    assert user_from_db["l_name"] == user_data["l_name"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]
    resp = client.post("/user/", data=json.dumps(user_data_same_email))
    assert resp.status_code == 503
    assert (
            'duplicate key value violates unique constraint "users_email_key"'
            in resp.json()["detail"]
    )


@pytest.mark.parametrize(
    "user_data_for_creation, expected_status_code, expected_detail",
    [
        (
            {},
            422,
            {
                "detail": [
                    {
                        'type': 'missing',
                        'loc': ['body', 'f_name'],
                        'msg': 'Field required',
                        'input': {},
                        'url': 'https://errors.pydantic.dev/2.4/v/missing'
                    },
                    {
                        'type': 'missing',
                        'loc': ['body', 'l_name'],
                        'msg': 'Field required',
                        'input': {},
                        'url': 'https://errors.pydantic.dev/2.4/v/missing'
                    },
                    {
                        'type': 'missing',
                        'loc': ['body', 'email'],
                        'msg': 'Field required',
                        'input': {},
                        'url': 'https://errors.pydantic.dev/2.4/v/missing'
                    }
                ]
            },
        ),
        (
            {"f_name": 123, "l_name": 456, "email": "lol"},
            422,
            {
                "detail": [
                    {
                        'type': 'string_type',
                        'loc': ['body', 'f_name'],
                        'msg': 'Input should be a valid string',
                        'input': 123,
                        'url': 'https://errors.pydantic.dev/2.4/v/string_type'
                    },
                    {
                        'type': 'string_type',
                        'loc': ['body', 'l_name'],
                        'msg': 'Input should be a valid string',
                        'input': 456,
                        'url': 'https://errors.pydantic.dev/2.4/v/string_type'
                    },
                    {
                        'type': 'value_error',
                        'loc': ['body', 'email'],
                        'msg': 'value is not a valid email address: The email address is not valid. It must have '
                               'exactly one @-sign.',
                        'input': 'lol',
                        'ctx': {'reason': 'The email address is not valid. It must have exactly one @-sign.'}
                    }
                ]},
        ),
        (
            {"f_name": "Vladyslav", "l_name": 456, "email": "lol"},
            422,
            {
                'detail': [
                    {
                        'type': 'string_type',
                        'loc': ['body', 'l_name'],
                        'msg': 'Input should be a valid string',
                        'input': 456,
                        'url': 'https://errors.pydantic.dev/2.4/v/string_type'
                    },
                    {
                        'type': 'value_error',
                        'loc': ['body', 'email'],
                        'msg': 'value is not a valid email address: The email address is not valid. It must have '
                               'exactly one @-sign.',
                        'input': 'lol',
                        'ctx': {'reason': 'The email address is not valid. It must have exactly one @-sign.'}
                    }
                ]
            }
        ),
        (
            {"f_name": "Vladyslav", "l_name": "Yurchenko", "email": "lol"},
            422,
            {
                'detail': [
                    {
                        'type': 'value_error',
                        'loc': ['body', 'email'],
                        'msg': 'value is not a valid email address: The email address is not valid. It must have '
                               'exactly one @-sign.',
                        'input': 'lol',
                        'ctx': {'reason': 'The email address is not valid. It must have exactly one @-sign.'}
                    }
                ]
            }
        ),
    ],
)
async def test_create_user_validation_error(
        client, user_data_for_creation, expected_status_code, expected_detail
):
    resp = client.post("/user/", data=json.dumps(user_data_for_creation))
    data_from_resp = resp.json()
    assert resp.status_code == expected_status_code
    assert data_from_resp == expected_detail
