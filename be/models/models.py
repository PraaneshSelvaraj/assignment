from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, String, Boolean
from sqlalchemy.sql.expression import text

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text('now()'))

class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(Users.id), nullable=False) 
    is_member = Column(Boolean, server_default=text("TRUE"))
    is_aurthor = Column(Boolean, server_default=text("FALSE"))

class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    aurthor_id = Column(Integer, ForeignKey(Users.id), nullable=False)
    
class Borrowings(Base):
    __tablename__ = "borrowings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(Users.id), nullable=False) 
    book_id = Column(Integer, ForeignKey(Books.id), nullable=False)
    borrowed_at = Column(DateTime, nullable=False, server_default=text('now()'))
    is_returned = Column(Boolean, server_default=text("FALSE"))

