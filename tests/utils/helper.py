import random
import string

from fastapi.testclient import TestClient

from hashing import hashing
from models import usermodel


def user_authentication(client: TestClient, username: str, password: str):
    data = {"username": username, "password": password}
    request = client.post("/login", data=data)
    response = request.json()
    assert request.status_code == 200
    headers = {"Authorization": f"{response['token_type']} {response['access_token']}"}
    client.headers.update(headers)
    return client


def user_creation(username: str, session_maker):
    user = (
        session_maker.query(usermodel.UserModel)
        .filter(usermodel.UserModel.email == username)
        .first()
    )
    name = "unkown"
    admin = False
    password = "password"
    if not user:
        new_user = usermodel.UserModel(
            name=name,
            email=username,
            password=hashing.encoding_password(password),
            is_admin=admin,
        )
        session_maker.add(new_user)
        session_maker.commit()
        session_maker.refresh(new_user)
        data = {"username": username, "password": password}
        return data
    data = {"username": username, "password": password}
    return data


def random_char(y):
    return "".join(random.choice(string.ascii_letters) for x in range(y))
