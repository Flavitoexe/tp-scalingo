from pydantic import BaseModel, Field, EmailStr

from database import Base


class Users(BaseModel) :
    id: int
    name: str
    email: EmailStr
    password: str
    hashedPassword: str


class CreateUser(BaseModel) :
    name: str = Field(
        min_length=3,
        max_length=30
    )

    email: EmailStr

    password: str = Field(
        min_length=8
    )



class ResponseUser(BaseModel) :
    id: int
    email: EmailStr


class Token(BaseModel) :
    access_token: str
    token_type: str