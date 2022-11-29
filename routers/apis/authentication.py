from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from crud import crud_user

router = APIRouter(
    tags=["authentication"],
)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return crud_user.user_crud.user_login(form_data)
