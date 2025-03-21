from pydantic import BaseModel, validator

class BaseValidator:
    @validator("*", pre=True)
    def check_empty_string(cls, val):
        if val == "":
            raise ValueError(f"{val} cannot be an empty string")
        return val

class RegisterUser(BaseModel, BaseValidator):
    username: str
    password: str
    confirmpassword : str
    email : str

class RegisterBook(BaseModel, BaseValidator):
    name : str
    content : str
    aurthor_id : int

class Borrow(BaseModel, BaseValidator):
    user_id : int
    book_id : int