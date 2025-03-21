import re
from fastapi import status, Depends
from fastapi.responses import JSONResponse
from databases.postgreSql import get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from filters import requestFilter
from models import models
from utils import hashing

async def register_user(user: requestFilter.RegisterUser, db : Session = Depends(get_db)):
    if user.password != user.confirmpassword:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message" : "Password doesn't match", "data":{}})

    if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,content={"message":"Invalid email format", "data":{}})

    if not re.match(r"^[a-z0-9_]+$", user.username):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,content={"message":"Invalid username format", "data":{}})
    
    if not re.match(r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", user.password):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,content={"msg":"Password must contain at least 8 characters, including at least one uppercase letter, one lowercase letter, one digit, and one special character", "data" : {}})
    
    existing_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if existing_user:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message" : "Username already exists", "data" : {}})
    
    hash_pwd = hashing.pwd_context.hash(user.password.encode('utf-8'))
    print(user)
    newUser = models.Users(email=user.email, username=user.username, password = hash_pwd)
    db.add(newUser)
    db.commit()


    newRole = models.Roles(user_id=newUser.id)
    db.add(newRole)
    db.commit()

    db.refresh(newUser)
    return {"message": "User Registered successfully"}