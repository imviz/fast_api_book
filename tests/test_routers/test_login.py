class TestLogin:
    def test_login_succes(self, normal_user, user_creation):
        response = normal_user.post("/login", data=user_creation)
        assert response.status_code == 200

    def test_login_no_data_given_fail(self, normal_user):
        response = normal_user.post("/login")
        assert response.status_code == 422
