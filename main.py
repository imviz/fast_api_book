from fastapi import FastAPI

from db.database import session_maker
from db.initial import create_admin
from routers.apis import authentication, book, user

app = FastAPI()


app.include_router(user.router)
app.include_router(book.router)
app.include_router(authentication.router)


if __name__ == "main":
    create_admin(session_maker)
