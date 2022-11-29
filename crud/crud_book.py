from fastapi import HTTPException, status

from db import database
from models import bookmodel


class Book:
    def create_book(self, book_name, user_id):
        new_book = bookmodel.BookModel(name=book_name.name, user_id=user_id)
        database.session_maker.add(new_book)
        database.session_maker.commit()
        database.session_maker.refresh(new_book)
        return new_book

    def get_all_book(self, user_id, db):
        books = (
            db.query(bookmodel.BookModel)
            .filter(bookmodel.BookModel.user_id == user_id)
            .all()
        )
        return books

    def get_book(self, book_id, db):
        return (
            db.query(bookmodel.BookModel)
            .filter(bookmodel.BookModel.id == book_id)
            .first()
        )

    def update_book(self, book_id, user_id, book_name, db):
        book = (
            db.query(bookmodel.BookModel)
            .filter(bookmodel.BookModel.id == book_id)
            .first()
        )
        if book:
            if book.user_id == user_id:
                db.query(bookmodel.BookModel).filter(
                    bookmodel.BookModel.id == book_id
                ).update({"name": book_name.name})
                db.commit()
                return book
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="this is not your book id ",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"no book in this id {book_id}",
            )

    def delete_book(self, book_id, user_id, db):
        book = (
            db.query(bookmodel.BookModel)
            .filter(bookmodel.BookModel.id == book_id)
            .first()
        )
        if book:
            if book.user_id == user_id:
                db.query(bookmodel.BookModel).filter(
                    bookmodel.BookModel.id == book_id
                ).delete(synchronize_session=False)
                db.commit()
                return {"detail": f"deleted {book_id}"}

            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="this is not your book id ",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"no book in this id {book_id}",
            )


crud_book = Book()
