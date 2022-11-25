from ..utils import helper


class TestAdmin:
    def test_create_user_success(self, admin_authentication):
        name = helper.random_char(5)
        email = helper.random_char(7) + "@gmail.com"
        data = {"name": name, "email": email, "password": "password"}
        session = admin_authentication
        response = session.post("/user", json=data)
        assert response.status_code == 201
        assert response.json()["email"] == email

    def test_create_user_no_data_given_fail(self, admin_authentication):
        session = admin_authentication
        response = session.post("/user")
        assert response.status_code == 422

    def test_get_all_user_success(self, admin_authentication):
        session = admin_authentication
        response = session.get("/user")
        assert response.status_code == 200

    def test_get_all_user(self, user_authentication):
        session = user_authentication
        response = session.get("/user")
        assert response.status_code == 404
