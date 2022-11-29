from db import database
from hashing.hashing import encoding_password
from models import usermodel


class User:
    def user_exists(self, userdata, db):
        user = (
            db.query(usermodel.UserModel)
            .filter(usermodel.UserModel.email == userdata.username)
            .first()
        )
        return user

    def user_create(self, userdata, db):
        new_user = usermodel.UserModel(
            name=userdata.name,
            email=userdata.email,
            password=encoding_password(userdata.password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def all_user_getting(self):
        users = (
            database.session_maker.query(usermodel.UserModel)
            .filter(usermodel.UserModel.is_admin == False)
            .all()
        )
        return users


user_crud = User()
