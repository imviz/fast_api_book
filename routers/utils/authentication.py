from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from db import database
from hashing.hashing import verify_password
from models import usermodel

from .jwt_token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter(
    tags=["authentication"],
)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    userz = (
        database.session_maker.query(usermodel.UserModel)
        .filter(usermodel.UserModel.email == form_data.username)
        .first()
    )
    if not userz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="invalid credential"
        )
    print(userz)
    if not verify_password(form_data.password, userz.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="password missmatch"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": userz.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
