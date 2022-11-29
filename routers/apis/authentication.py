from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from crud import crud_user
from db import database
from hashing import hashing

from ..utils import jwt_token

router = APIRouter(
    tags=["authentication"],
)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud_user.user_crud.user_exists(form_data, db=database.session_maker)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="invalid credential"
        )

    if not hashing.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="password missmatch"
        )
    access_token = jwt_token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
