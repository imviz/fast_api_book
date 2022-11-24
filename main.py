from fastapi import FastAPI

from models.db import session_maker
from models.initial import create_admin
from routers import authentication, book, user

app = FastAPI()


app.include_router(user.router)
app.include_router(book.router)
app.include_router(authentication.router)


if __name__ == "main":
    create_admin(session_maker)
