from typing import List, Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    email: str
    name: str
    password: str


class BookSchema(BaseModel):
    name: str


class UpdateBookSchema(BaseModel):
    name: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class LoginSchema(BaseModel):
    email: str
    password: str
