from db import database
from hashing.hashing import encoding_password
from models import usermodel


class User:
    def user_create(self, request):
        new_user = usermodel.UserModel(
            name=request.name,
            email=request.email,
            password=encoding_password(request.password),
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
