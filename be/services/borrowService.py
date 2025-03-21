import re
from fastapi import status, Depends
from fastapi.responses import JSONResponse
from databases.postgreSql import get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from filters import requestFilter
from models import models
from utils import serialize

async def borrow(b: requestFilter.Borrow, db : Session = Depends(get_db)):
    existing_user = db.query(models.Users).filter(models.Users.id == b.user_id).first()
    if not existing_user:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message" : "User doesnt exists", "data" : {}})
    
    book = db.query(models.Books).filter(models.Books.id == b.book_id).first()
    if not book:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message" : "Book doesnt exists", "data" : {}})

    bo = db.query(models.Borrowings).filter(models.Borrowings.user_id == b.user_id and models.Borrowings.book_id == b.book_id).first()
    if bo:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message" : "Book already borrowed", "data" : {}})

        
    new_borrowings = models.Borrowings(user_id = b.user_id, book_id = b.book_id)
    db.add(new_borrowings)
    db.commit()
    db.refresh(new_borrowings)
    return {"message" : "Book has been Successfully Borrowed"}

async def get_borrowings(db : Session = Depends(get_db)):
    results = db.query(models.Borrowings).all()
    borrowings = serialize.serialize_get_borrowings(results)
    return {"message" : "Listing Borrowing", "data" : {"borrowings" : borrowings}}

async def return_book(id : int, db : Session = Depends(get_db)):
    exisiting_borrowing = db.query(models.Borrowings).filter(models.Borrowings.id == id).first()
    if not exisiting_borrowing:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message" : "Borrowing not exists", "data" : {}})
    
    exisiting_borrowing.is_returned = True
    db.add(exisiting_borrowing)
    db.commit()
    return{"message" : "Book has been returned"}
        
async def get_borrowing(id : int, db : Session = Depends(get_db)):
    exisiting_borrowing = db.query(models.Borrowings).filter(models.Borrowings.id == id).first()
    if not exisiting_borrowing:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message" : "Borrowing not exists", "data" : {}})
    
    resp = serialize.serialize_borrowing(exisiting_borrowing)
    return {"message" : "Borrowing has been fetched", "data" : {"borrowing" : resp}}