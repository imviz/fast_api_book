def test_create_user_success(admin_user_token):
    data = {"name": "user1234", "email": "user@12345.com", "password": "password"}
    response = admin_user_token.post("/user", json=data)
    assert response.status_code == 201
    assert response.json()["email"] == "user@12345.com"


def test_create_user_fail(admin_user_token):
    data = {"name": "user123", "email": "user@123.com", "password": "password"}
    response = admin_user_token.post("/user", data=data)
    assert response.status_code == 422


def test_get_all_user_success(admin_user_token):
    response = admin_user_token.get("/user")
    assert response.status_code == 200
