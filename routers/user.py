from fastapi import APIRouter, Depends, HTTPException, status

from hashing.hashing import encoding_password
from models import db, usermodel
from schema.schema import TokenData, UserSchema

from .oauth2 import get_current_user

router = APIRouter(
    tags=["user"],
    prefix="/user",
)

# admin can only create user


@router.post("/")
def create_user(
    request: UserSchema, current_user: TokenData = Depends(get_current_user)
):
    user = (
        db.session_maker.query(usermodel.UserModel)
        .filter(usermodel.UserModel.email == current_user.email)
        .first()
    )
    if user.is_admin:
        hashed_pass = encoding_password(request.password)
        new_user = usermodel.UserModel(
            name=request.name, email=request.email, password=hashed_pass
        )
        db.session_maker.add(new_user)
        db.session_maker.commit()
        db.session_maker.refresh(new_user)
        return new_user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="you have no permission to create a user",
        )
