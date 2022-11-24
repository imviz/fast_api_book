def test_login_succes(normal_user):
    data = {"username": "vishnu@e.com", "password": "password"}
    response = normal_user.post("/login", data=data)
    assert response.status_code == 200


def test_login_fail(normal_user):
    data = {"username": "gagagag@jhfd.com", "password": "34343"}
    response = normal_user.post("/login", data=data)
    assert response.status_code == 404
