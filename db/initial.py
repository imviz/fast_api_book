from hashing.hashing import encoding_password
from models import usermodel

INI_EMAIL = "vishnu@e.com"
INI_NAME = "vishnu"
INI_PASSWORD = "password"
INI_ADMIN = True


def create_admin(db):
    admin = (
        db.query(usermodel.UserModel)
        .filter(usermodel.UserModel.email == INI_EMAIL)
        .first()
    )
    if not admin:
        hashed_pass = encoding_password(INI_PASSWORD)
        new_user = usermodel.UserModel(
            name=INI_NAME, email=INI_EMAIL, password=hashed_pass, is_admin=INI_ADMIN
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    else:
        print("admin already created")
