import json
from uuid import uuid4

# Тест для создания пользователя
import pytest


async def test_create_user(client, get_user_from_database):
    # Данные нового пользователя
    user_data = {
        'f_name': 'Vld',
        'l_name': 'Yrchnk',
        'email': 'vld.yrchnk@gmail.com',
    }
    # Отправка POST-запроса на создание пользователя
    resp = client.post("/user/", data=json.dumps(user_data))
    # Проверка успешного ответа от сервера
    assert resp.status_code == 200
    # Извлечение данных из ответа в формате JSON
    data_from_resp = resp.json()
    # Проверка соответствия данных запроса данным из ответа
    assert data_from_resp["f_name"] == user_data["f_name"]
    assert data_from_resp["l_name"] == user_data["l_name"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    # Получение пользователя из тестовой базы данных по ID
    user_from_db = await get_user_from_database(data_from_resp["user_id"])
    # Проверка, что в базе данных есть одна запись о пользователе
    assert len(user_from_db) == 1
    # Извлечение данных из записи в базе данных
    user_from_db = dict(user_from_db[0])
    # Проверка соответствия данных из базы данных данным из запроса
    assert user_from_db["f_name"] == user_data["f_name"]
    assert user_from_db["l_name"] == user_data["l_name"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]


async def test_delete_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        'user_id': uuid4(),
        'f_name': 'Filip',
        'l_name': 'Fry',
        'email': 'fry42@futurama.ua',
        'is_active': True,
    }
    await create_user_in_database(**user_data)
    resp = client.delete(f"/user/?user_id={user_data['user_id']}")
    assert resp.status_code == 200
    assert resp.json() == {"deleted_user_id": str(user_data['user_id'])}
    users_from_db = await get_user_from_database(user_data['user_id'])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["f_name"] == user_data["f_name"]
    assert user_from_db["l_name"] == user_data["l_name"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is False
    assert user_from_db["user_id"] == user_data["user_id"]


async def test_get_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        'user_id': uuid4(),
        'f_name': 'Filip',
        'l_name': 'Fry',
        'email': 'fry42@futurama.ua',
        'is_active': True,
    }
    await create_user_in_database(**user_data)
    resp = client.get(f"/user/?user_id={user_data['user_id']}")
    assert resp.status_code == 200
    users_from_response = resp.json()
    assert users_from_response["user_id"] == str(user_data["user_id"])
    assert users_from_response["f_name"] == user_data["f_name"]
    assert users_from_response["l_name"] == user_data["l_name"]
    assert users_from_response["email"] == user_data["email"]
    assert users_from_response["is_active"] == user_data["is_active"]


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
    resp = client.patch(f"/user/?user_id={user_data['user_id']}", data=json.dumps(user_data_updated))
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


@pytest.mark.parametrize("user_data_updated, expected_status_code, expected_detail", [
    (
            {},
            422,
            {"detail": "At least one parameter for user update info should be provided"}
    ),
    (
            {"f_name": "123"},
            422,
            {"detail": "First name should contains only letters"}
    ),
    (
            {"l_name": "123"},
            422,
            {"detail": "Last name should contains only letters"}
    ),
    (
            {"f_name": ""},
            422,
            {"detail": [
                {
                    'type': 'string_too_short',
                    'loc': ['body', 'f_name'],
                    'msg': 'String should have at least 1 characters',
                    'input': '',
                    'ctx': {'min_length': 1},
                    'url': 'https://errors.pydantic.dev/2.4/v/string_too_short'
                }
            ]}
    ),
    (
            {"l_name": ""},
            422,
            {"detail": [
                {
                    'type': 'string_too_short',
                    'loc': ['body', 'l_name'],
                    'msg': 'String should have at least 1 characters',
                    'input': '',
                    'ctx': {'min_length': 1},
                    'url': 'https://errors.pydantic.dev/2.4/v/string_too_short'
                }
            ]}
    ),
    (
            {"email": ""},
            422,
            {'detail': [
                {
                    'type': 'value_error',
                    'loc': ['body', 'email'],
                    'msg': 'value is not a valid email address: The email address is not valid. It must have exactly '
                           'one @-sign.',
                    'input': '',
                    'ctx': {'reason': 'The email address is not valid. It must have exactly one @-sign.'}
                }
            ]}
    ),
    (
            {"email": "123"},
            422,
            {'detail': [
                {
                    'type': 'value_error',
                    'loc': ['body', 'email'],
                    'msg': 'value is not a valid email address: The email address is not valid. It must have exactly '
                           'one @-sign.',
                    'input': '123',
                    'ctx': {'reason': 'The email address is not valid. It must have exactly one @-sign.'}
                 }
            ]}
    ),
])
async def test_update_user_validation_error(client, create_user_in_database, get_user_from_database, user_data_updated,
                                            expected_status_code, expected_detail):
    user_data = {
        "user_id": uuid4(),
        "f_name": "Vlad",
        "l_name": "Yurchenko",
        "email": "vld.yrchnk@gmail.com",
        "is_active": True,
    }
    await create_user_in_database(**user_data)
    resp = client.patch(f"/user/?user_id={user_data['user_id']}", data=json.dumps(user_data_updated))
    assert resp.status_code == expected_status_code
    resp_data = resp.json()
    assert resp_data == expected_detail
