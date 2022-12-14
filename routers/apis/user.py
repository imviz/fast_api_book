from typing import List

from fastapi import APIRouter, Depends, status

from crud import crud_user
from db import database
from schema.schema import TokenData, UserSchema, UserShowSchema

from ..utils.oauth2 import get_admin_user

router = APIRouter(
    tags=["user"],
    prefix="/user",
)


@router.post("/", response_model=UserShowSchema, status_code=status.HTTP_201_CREATED)
def create_user(
    userdata: UserSchema, current_user: TokenData = Depends(get_admin_user)
):
    return crud_user.user_crud.user_create(userdata=userdata, db=database.session_maker)


@router.get("/", response_model=List[UserShowSchema], status_code=status.HTTP_200_OK)
def get_all_user(current_user: TokenData = Depends(get_admin_user)):

    return crud_user.user_crud.all_user_getting()
