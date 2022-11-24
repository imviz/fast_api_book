import pytest
from fastapi.testclient import TestClient
from utils import authentication

from main import app
from models.db import session_maker

client = TestClient(app)

generated_email = authentication.random_char(7) + "@gmail.com"
ADMIN_EMAIL = "vishnu@e.com"
ADMIN_PASSWORD = "password"
user_email = "anu@es.com"


@pytest.fixture(scope="module")
def admin_user_token():
    return authentication.authentication_headers(
        client=client, email=ADMIN_EMAIL, password=ADMIN_PASSWORD
    )


@pytest.fixture(scope="module")
def normal_user_token_headers():
    return authentication.authentication_from_email(
        client=client, email=user_email, session_maker=session_maker
    )


@pytest.fixture(scope="module")
def normal_user():
    return client
