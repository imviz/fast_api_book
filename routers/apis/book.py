from typing import List

from fastapi import APIRouter, Depends, status

from crud import crud_book
from models import bookmodel
from schema.schema import BookSchema, BookUserSchema, TokenData

from ..utils.oauth2 import get_current_user

router = APIRouter(
    tags=["book"],
    prefix="/book",
)


@router.post("/", response_model=BookUserSchema, status_code=status.HTTP_201_CREATED)
def create_book(
    book_name: BookSchema, current_user: TokenData = Depends(get_current_user)
):
    return crud_book.crud_book.create_book(book_name, current_user.id)


@router.get("/", response_model=List[BookUserSchema], status_code=status.HTTP_200_OK)
def get_all_book(current_user: TokenData = Depends(get_current_user)):
    return crud_book.crud_book.get_all_book(user_id=current_user.id)


@router.get("/{id}", response_model=BookUserSchema, status_code=status.HTTP_200_OK)
def get_book(id, current_user: TokenData = Depends(get_current_user)):
    return crud_book.crud_book.get_book(book_id=id, user_id=current_user.id)


@router.put("/{id}", response_model=BookUserSchema, status_code=status.HTTP_200_OK)
def update_book(
    id, book_name: BookSchema, current_user: TokenData = Depends(get_current_user)
):
    return crud_book.crud_book.update_book(
        book_name=book_name, user_id=current_user.id, book_id=id
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_book(id, current_user: TokenData = Depends(get_current_user)):
    return crud_book.crud_book.delete_book(user_id=current_user.id, book_id=id)
