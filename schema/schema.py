from typing import List, Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    email: str
    name: str
    password: str


class UserShowSchema(BaseModel):
    email: str
    name: str

    class Config:
        orm_mode = True


class BookSchema(BaseModel):
    name: str


class BookUserSchema(BaseModel):
    name: str
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    id: int


class LoginSchema(BaseModel):
    email: str
    password: str
