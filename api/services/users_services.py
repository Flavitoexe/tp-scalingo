from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from models.Users import Users
from schemas.Users import CreateUser
from database import getDb


SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

passwordHash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hashPassword(password: str) :
    return passwordHash.hash(password)

def verifyPassword(
    password: str, 
    hashed: str
) :
    return passwordHash.verify(password, hashed)

def createAccessToken(username: str) :
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": username,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        ALGORITHM
    )


def register(
    userData: CreateUser,
    db: Session
) :

    user = db.query(Users).filter(Users.name == userData.name).first()
    if user :
        raise HTTPException(
            status_code=409,
            detail="Username already taken."
        )

    newUser = Users(
        name=userData.name, 
        email=userData.email, 
        hashedPassword=hashPassword(userData.password)
    )

    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return{
        "message": "User created successfully."
    }


def login(
    userData: OAuth2PasswordRequestForm,
    db: Session
) :

    user = db.query(Users).filter(Users.name == userData.username).first()
    if user is None :
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials."
        )

    if not verifyPassword(
        userData.password,
        user.hashedPassword
    ) :
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials."
        )

    token = createAccessToken(user.name)

    return {
        "access_token": token,
        "token_type": "Bearer"
    }


def getCurrentUser(
    db: Session = Depends(getDb),
    token: str = Depends(oauth2_scheme)
) :
    try :
        payload = jwt.decode(
            token,
            SECRET_KEY,
            ALGORITHM
        )

        username = payload.get("sub")
        if username is None :
            raise HTTPException(
                status_code=401,
                detail="Invalid or absent token."
            )

        user = db.query(Users).filter(Users.name == username).first()
        if user is None :
            raise HTTPException(
                status_code=404,
                detail="User with this name doesn't exist."
            )

        return user
    except JWTError :
        raise HTTPException(
            status_code=401,
            detail="Invalid or absent token."
        )