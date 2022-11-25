from fastapi import APIRouter, Depends, HTTPException, status

from db import database
from hashing.hashing import encoding_password
from models import usermodel
from schema.schema import TokenData, UserSchema

from ..utils.oauth2 import get_current_user

router = APIRouter(
    tags=["user"],
    prefix="/user",
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
    request: UserSchema, current_user: TokenData = Depends(get_current_user)
):
    user = (
        database.session_maker.query(usermodel.UserModel)
        .filter(usermodel.UserModel.email == current_user.email)
        .first()
    )
    if user.is_admin:
        hashed_pass = encoding_password(request.password)
        new_user = usermodel.UserModel(
            name=request.name, email=request.email, password=hashed_pass
        )
        database.session_maker.add(new_user)
        database.session_maker.commit()
        database.session_maker.refresh(new_user)
        return new_user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="you have no permission to create a user",
        )


@router.get("/")
def get_all_user(current_user: TokenData = Depends(get_current_user)):
    user = (
        database.session_maker.query(usermodel.UserModel)
        .filter(usermodel.UserModel.email == current_user.email)
        .first()
    )
    if user.is_admin:
        users = (
            database.session_maker.query(usermodel.UserModel)
            .filter(usermodel.UserModel.is_admin == False)
            .all()
        )
        return users
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="you have no permission to see user list",
        )
