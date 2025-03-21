from fastapi import status, Depends
from fastapi.responses import JSONResponse
from databases.postgreSql import get_db
from sqlalchemy.orm import Session
from filters import requestFilter
from models import models
from utils import serialize


async def register_book(user: requestFilter.RegisterBook, db : Session = Depends(get_db)):
    new_book = models.Books(name = user.name, content = user.content, aurthor_id = user.aurthor_id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {"message" : "Book has been added"}

async def get_books(db: Session = Depends(get_db)):
    results = db.query(models.Books).all()
    books = serialize.serialize_get_books(results)
    return {"message" : "List of available books", "data" : {"books" : books}}

async def get_book(book_id : int, db: Session = Depends(get_db)):
    resp = db.query(models.Books).filter(models.Books.id == book_id).first()
    if not resp: 
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message" : "Book not exists", "data" : {}})
    
    book = serialize.serialize_book(resp)
    return {"message" : "Book retrievied Successfully.", "data" : {"book" : book}}

async def delete_book(book_id : int, db: Session = Depends(get_db)):
    book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if not book: 
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message" : "Book not exists", "data" : {}})
    
    db.delete(book)
    db.commit()

async def update_book(book_id : int, book: requestFilter.RegisterBook, db: Session = Depends(get_db)):
    existing_book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if not book: 
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message" : "Book not exists", "data" : {}})
    
    existing_book.name = book.name
    existing_book.content = book.content
    existing_book.aurthor_id = book.aurthor_id
    db.add(existing_book)
    db.commit()
    return {"message" : "Book has been updated"}