from fastapi import APIRouter, status, Depends
from sqlalchemy.orm.session import Session
from databases.postgreSql import get_db
from filters import requestFilter, responseFilter
from services import borrowService

router = APIRouter()

@router.post("/borrowings", status_code=status.HTTP_201_CREATED, response_model=responseFilter.Response)
async def borrow(b: requestFilter.Borrow, db : Session = Depends(get_db)):
    return await borrowService.borrow(b, db)

@router.get("/borrowings", status_code=status.HTTP_200_OK,  response_model=responseFilter.Response)
async def get_borrowings(db : Session = Depends(get_db)):
    return await borrowService.get_borrowings(db)

@router.put("/borrowings/{id}/return", status_code=status.HTTP_200_OK, response_model=responseFilter.Response)
async def return_book(id : int, db : Session = Depends(get_db)):
    return await borrowService.return_book(id, db)

@router.get("/borrowings/{id}", status_code=status.HTTP_200_OK,  response_model=responseFilter.Response)
async def get_borrowing(id : int,db : Session = Depends(get_db)):
    return await borrowService.get_borrowing(id, db)