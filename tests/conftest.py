import pytest
from fastapi.testclient import TestClient

from db.database import session_maker
from main import app
from tests.utils import helper

client = TestClient(app)

generated_email = helper.random_char(7) + "@gmail.com"
ADMIN_EMAIL = "vishnu@e.com"
ADMIN_PASSWORD = "password"


@pytest.fixture(scope="module")
def normal_user():
    return client


@pytest.fixture(scope="module")
def admin_authentication():
    return helper.user_authentication(
        client=client, username=ADMIN_EMAIL, password=ADMIN_PASSWORD
    )


@pytest.fixture(scope="module")
def user_creation():
    return helper.user_creation(username=generated_email, session_maker=session_maker)


@pytest.fixture(scope="module")
def user_authentication(user_creation):
    return helper.user_authentication(
        client=client,
        username=user_creation["username"],
        password=user_creation["password"],
    )


@pytest.fixture(scope="module")
def testuser_creation_and_authentication():
    data = helper.user_creation(username=generated_email, session_maker=session_maker)
    return helper.user_authentication(
        client=client, username=data["username"], password=data["password"]
    )


@pytest.fixture(scope="module")
def create_book(user_authentication):
    name = helper.random_char(7)
    data = {"name": name}
    session = user_authentication
    response = session.post("/book", json=data)
    value = response.json()
    return value
