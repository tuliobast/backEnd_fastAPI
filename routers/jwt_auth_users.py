from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "96f39524dd4298f1fcd1fb6f58e99b7428b303916759688debe7738494a63e92"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool


class UserDB(User):
    password: str


users_db = {
    "tuliobast": {
        "username": "tuliobast",
        "full_name": "tulio bastidas",
        "email": "tuliobast@gmail.com",
        "disable": False,
        "password": "$2a$12$7g8do9.soTFaMfaQNcqtYuPK4BPOHPyjsqc9DCEI76xM/RZSFrdTy"
    },
    "tuliobast2": {
        "username": "tuliobast2",
        "full_name": "tulio bastidas 2",
        "email": "tuliobast2@gmail.com",
        "disable": True,
        "password": "$2a$12$oeyvwjx/uPygzWe8GHKDKu6k.6jZChdZkDYYUuey7tVfUdRqE031e"
    } 
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

    
async def auth_user(token: str = Depends(oauth2)):

    exception= HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail= "Credenciales de autenticacion invalidas",
            headers= {"WWW-Authenticate": "Bearer"})

    try:
        username= jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None: 
            raise exception
        
    except JWTError:
         raise exception

    return search_user(username)
 
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Usuario inactivo")
    
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm= Depends()):
    user_db= users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail= "El usuario no es correcto")
    
    user= search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "La contraseña no es correcto")
    
    access_token= {"sub": user.username, 
                   "exp": datetime.utcnow()+ timedelta(minutes= ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token,
                                       SECRET,
                                       access_token=ALGORITHM),
            "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user


