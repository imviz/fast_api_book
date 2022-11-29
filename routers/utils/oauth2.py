from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from db import database
from models import usermodel

from .jwt_token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)


def get_admin_user(current_user=Depends(get_current_user)):
    user = (
        database.session_maker.query(usermodel.UserModel)
        .filter(usermodel.UserModel.email == current_user.email)
        .first()
    )

    if user.is_admin:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="you are no permission to access here",
        )
