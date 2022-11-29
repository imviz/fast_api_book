from datetime import datetime, timedelta

from jose import JWTError, jwt

from db import database
from models import usermodel
from schema.schema import TokenData

from . import config

SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = (
            database.session_maker.query(usermodel.UserModel)
            .filter(usermodel.UserModel.email == email)
            .first()
        )
        token_data = TokenData(email=email, id=user.id)
        return token_data

    except JWTError:
        raise credentials_exception
