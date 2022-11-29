from datetime import timedelta

from fastapi import HTTPException, status

from db import database
from hashing import hashing
from hashing.hashing import encoding_password
from models import usermodel
from routers.utils import config, jwt_token


class User:
    def user_login(self, userdata):
        user = (
            database.session_maker.query(usermodel.UserModel)
            .filter(usermodel.UserModel.email == userdata.username)
            .first()
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="invalid credential"
            )

        if not hashing.verify_password(userdata.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="password missmatch"
            )

        # access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = jwt_token.create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    def user_create(self, userdata):
        new_user = usermodel.UserModel(
            name=userdata.name,
            email=userdata.email,
            password=encoding_password(userdata.password),
        )
        database.session_maker.add(new_user)
        database.session_maker.commit()
        database.session_maker.refresh(new_user)
        return new_user

    def all_user_getting(self):
        users = (
            database.session_maker.query(usermodel.UserModel)
            .filter(usermodel.UserModel.is_admin == False)
            .all()
        )
        return users


user_crud = User()
