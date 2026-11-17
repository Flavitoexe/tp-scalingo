from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas.Users import Users, CreateUser
from services.users_services import register, login
from database import getDb


router = APIRouter(prefix="/auth")


@router.get("/me")
def getMe() :
    return "ok"


@router.post("/register")
def registerUser(
    userData: CreateUser,
    db: Session = Depends(getDb)
) :
    return register(userData, db)


@router.post("/login") 
def loginUser(
    userData: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(getDb)
) :
    return login(userData, db)