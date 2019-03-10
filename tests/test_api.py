from jasmine_app.models.user import User


def test_user(client):

    user_id = 1
    user_data = {"name": "test_1", "id": 1, "password": 123}

    res = client.post("/api/user", json=user_data)
    assert res.status_code == 200
    assert User.select().count() == 1

    res = client.get("/api/user?user_id={user_id}".format(user_id=user_id))
    assert res.status_code == 200
