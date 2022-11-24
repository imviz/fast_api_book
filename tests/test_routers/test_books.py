def test_create_book_sucess(normal_user_token_headers):
    data = {"name": "mybooks"}
    response = normal_user_token_headers.post("/book", json=data)
    assert response.status_code == 201
    assert response.json()["name"] == "mybooks"


def test_create_book_fail(normal_user_token_headers):
    response = normal_user_token_headers.post("/book")
    assert response.status_code == 422


def test_get_book_by_id_success(normal_user_token_headers):
    response = normal_user_token_headers.get("/book/12")
    assert response.status_code == 200
    assert response.json()["name"] == "mybooks"


def test_get_all_books_fail(normal_user_token_headers):
    response = normal_user_token_headers.get("/book/9000")
    assert response.status_code == 404


def test_get_all_books_success(normal_user_token_headers):
    response = normal_user_token_headers.get("/book")
    assert response.status_code == 200


def test_update_book_success(normal_user_token_headers):
    data = {"name": "bookworld"}
    response = normal_user_token_headers.put("/book/7", json=data)
    assert response.status_code == 200
    assert response.json()["name"] == "bookworld"


def test_update_book_fail(normal_user_token_headers):
    data = {"name": "bookworld"}
    response = normal_user_token_headers.put("/book/7", data=data)
    assert response.status_code == 422


def test_delete_book_success(normal_user_token_headers):
    response = normal_user_token_headers.delete("/book/19")
    print(response.json())
    assert response.status_code == 200


def test_delete_book_fail(normal_user_token_headers):
    response = normal_user_token_headers.delete("/book/90")
    assert response.status_code == 404
