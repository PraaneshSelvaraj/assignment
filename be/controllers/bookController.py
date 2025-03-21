from fastapi import APIRouter, status, Depends
from sqlalchemy.orm.session import Session
from databases.postgreSql import get_db
from filters import requestFilter, responseFilter
from services import bookService

router = APIRouter()

@router.post("/books", status_code=status.HTTP_201_CREATED, response_model=responseFilter.Response)
async def register_book(book: requestFilter.RegisterBook, db : Session = Depends(get_db)):
    return await bookService.register_book(book, db)

@router.get("/books", status_code=status.HTTP_200_OK, response_model=responseFilter.Response)
async def get_books(db: Session = Depends(get_db)):
    return await bookService.get_books(db)

@router.get("/books/{book_id}", status_code=status.HTTP_200_OK, response_model=responseFilter.Response  )
async def get_book(book_id, db: Session = Depends(get_db)):
    return await bookService.get_book(book_id, db)

@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id, db: Session = Depends(get_db)):
    await bookService.delete_book(book_id, db)

@router.put("/books/{book_id}", status_code=status.HTTP_200_OK, response_model=responseFilter.Response)
async def register_book(book_id : int, book: requestFilter.RegisterBook,db : Session = Depends(get_db)):
    return await bookService.update_book(book_id, book, db)