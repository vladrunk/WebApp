import json


async def test_create_user(client, get_user_from_database):
    user_data = {
        'f_name': 'Vld',
        'l_name': 'Yrchnk',
        'email': 'vld.yrchnk@gmail.com',
    }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["f_name"] == user_data["f_name"]
    assert data_from_resp["l_name"] == user_data["l_name"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    user_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(user_from_db) == 1
    user_from_db = dict(user_from_db[0])
    assert user_from_db["f_name"] == user_data["f_name"]
    assert user_from_db["l_name"] == user_data["l_name"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]
