from fastapi import APIRouter, status, Depends
from sqlalchemy.orm.session import Session
from databases.postgreSql import get_db
from filters import requestFilter, responseFilter
from services import userAuthService

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=responseFilter.Response)
async def register_user(user: requestFilter.RegisterUser,db : Session = Depends(get_db)):
    return await userAuthService.register_user(user, db)


async def register_user():
    return "Hello"