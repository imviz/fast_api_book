from fastapi import APIRouter, Depends, HTTPException, status

from db import database
from models import bookmodel, usermodel
from schema.schema import BookSchema, TokenData, UpdateBookSchema

from ..utils.oauth2 import get_current_user

router = APIRouter(
    tags=["book"],
    prefix="/book",
)

# admin can only create book


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_book(
    request: BookSchema, current_user: TokenData = Depends(get_current_user)
):
    userz = (
        database.session_maker.query(usermodel.UserModel)
        .filter(usermodel.UserModel.email == current_user.email)
        .first()
    )
    new_book = bookmodel.BookModel(name=request.name, user_id=userz.id)
    database.session_maker.add(new_book)
    database.session_maker.commit()
    database.session_maker.refresh(new_book)
    return new_book


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_book(current_user: TokenData = Depends(get_current_user)):
    userz = (
        database.session_maker.query(usermodel.UserModel)
        .filter(usermodel.UserModel.email == current_user.email)
        .first()
    )
    books = (
        database.session_maker.query(bookmodel.BookModel)
        .filter(bookmodel.BookModel.user_id == userz.id)
        .all()
    )

    if books:
        return books
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no book in your hand"
        )


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_book(id, current_user: TokenData = Depends(get_current_user)):
    bookz = (
        database.session_maker.query(bookmodel.BookModel)
        .filter(bookmodel.BookModel.id == id)
        .first()
    )
    userz = (
        database.session_maker.query(usermodel.UserModel)
        .filter(usermodel.UserModel.email == current_user.email)
        .first()
    )
    if bookz:
        if userz.id == bookz.user_id:
            books = (
                database.session_maker.query(bookmodel.BookModel)
                .filter(bookmodel.BookModel.id == id)
                .first()
            )
            return books
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="this is not your book id ",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no book in this id {id}"
        )


@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_book(
    id, request: UpdateBookSchema, current_user: TokenData = Depends(get_current_user)
):
    bookz = (
        database.session_maker.query(bookmodel.BookModel)
        .filter(bookmodel.BookModel.id == id)
        .first()
    )
    userz = (
        database.session_maker.query(usermodel.UserModel)
        .filter(usermodel.UserModel.email == current_user.email)
        .first()
    )
    if bookz:
        if userz.id == bookz.user_id:
            database.session_maker.query(bookmodel.BookModel).filter(
                bookmodel.BookModel.id == id
            ).update({"name": request.name})
            database.session_maker.commit()
            return request
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="this is not your book ,cannot update this book ",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no book in this id {id}"
        )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_book(id, current_user: TokenData = Depends(get_current_user)):
    bookz = (
        database.session_maker.query(bookmodel.BookModel)
        .filter(bookmodel.BookModel.id == id)
        .first()
    )
    userz = (
        database.session_maker.query(usermodel.UserModel)
        .filter(usermodel.UserModel.email == current_user.email)
        .first()
    )
    if bookz:
        if userz.id == bookz.user_id:
            database.session_maker.query(bookmodel.BookModel).filter(
                bookmodel.BookModel.id == id
            ).delete(synchronize_session=False)
            database.session_maker.commit()
            return {"detail": f"deleted {id}"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="this is not your book ,no permission to delete the book",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no book in this id {id}"
        )
