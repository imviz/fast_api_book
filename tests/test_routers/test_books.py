import pytest

from ..utils import helper


class TestBook:
    def test_create_book_sucess(self, user_authentication):
        name = helper.random_char(7)
        data = {"name": name}
        session = user_authentication
        response = session.post("/book", json=data)
        assert response.status_code == 201
        assert response.json()["name"] == name

    def test_get_book_by_id_success(self, user_authentication, create_book):
        session = user_authentication
        id = create_book["id"]
        response = session.get(f"/book/{id}")
        assert response.status_code == 200
        assert response.json()["name"] == create_book["name"]

    def test_get_all_books_success(self, user_authentication):
        session = user_authentication
        response = session.get("/book")
        assert response.status_code == 200

    def test_update_book_success(self, user_authentication, create_book):
        name = helper.random_char(5)
        data = {"name": name}
        session = user_authentication
        id = create_book["id"]
        response = session.put(f"/book/{id}/", json=data)
        assert response.status_code == 200
        assert response.json()["name"] == name

    def test_delete_book_success(self, user_authentication, create_book):
        session = user_authentication
        id = create_book["id"]
        print(id, "rbntt")
        response = session.delete(f"/book/{id}")
        assert response.status_code == 200

    def test_create_book_no_data_given_fail(self, user_authentication):
        session = user_authentication
        response = session.post("/book")
        assert response.status_code == 422

    def test_get_book_by_id_other_user_access_fail(
        self, admin_authentication, create_book
    ):
        id = create_book["id"]
        response = admin_authentication.get(f"/book/{id}")
        assert response.status_code == 404

    def test_update_book_other_user_access_fail(
        self, admin_authentication, create_book
    ):
        name = helper.random_char(5)
        data = {"name": name}
        session = admin_authentication
        id = create_book["id"]
        response = session.put(f"/book/{id}", json=data)
        assert response.status_code == 404

    def test_delete_book_by_id_other_user_access_fail(
        self, admin_authentication, create_book
    ):
        id = create_book["id"]
        response = admin_authentication.delete(f"/book/{id}")
        assert response.status_code == 404
