import random
import string

from fastapi.testclient import TestClient

from hashing import hashing
from models import usermodel


def authentication_headers(client: TestClient, email: str, password: str):
    data = {"username": email, "password": password}
    request = client.post("/login", data=data)
    response = request.json()
    assert request.status_code == 200
    access_token = response["access_token"]
    headers = {"Authorization": f"{response['token_type']} {response['access_token']}"}
    client.headers.update(headers)
    return client


def authentication_from_email(client: TestClient, email: str, session_maker):
    user = (
        session_maker.query(usermodel.UserModel)
        .filter(usermodel.UserModel.email == email)
        .first()
    )
    name = "unkown"
    admin = True
    password = "password"
    if not user:
        new_user = usermodel.UserModel(
            name=name,
            email=email,
            password=hashing.encoding_password(password),
            is_admin=admin,
        )
        session_maker.add(new_user)
        session_maker.commit()
        session_maker.refresh(new_user)
        return authentication_headers(client=client, email=email, password=password)
    return authentication_headers(client=client, email=email, password=password)


def random_char(y):
    return "".join(random.choice(string.ascii_letters) for x in range(y))
