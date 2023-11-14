import json


# Тест для создания пользователя
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
