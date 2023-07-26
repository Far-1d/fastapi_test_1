from jose import JWTError, jwt
from . import schemas, database, models
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status #for get_current_user
from fastapi.security import OAuth2PasswordBearer #for oauth2 schema
from sqlalchemy.orm import Session
from .config import Setting
oaut2_scheme = OAuth2PasswordBearer(tokenUrl= "login")


SECRET = Setting.SECRET
ALGORITHM = Setting.ALGORITHM
ACCESS_TOKEN_EXPIRY_MINUTES = Setting.ACCESS_TOKEN_EXPIRY_MINUTES

def create_token (payload:dict[schemas.payload]):
    copy = payload.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRY_MINUTES)
    copy.update({"exp" : expire})

    encoded_jwt = jwt.encode(copy, SECRET, algorithm = ALGORITHM)

    return encoded_jwt

def verify_token(token:str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET, algorithms = [ALGORITHM])
        name: str = payload.get("user")

        if name is None :
            raise credentials_exception

        token_data = schemas.payload(user = name)

    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str= Depends(oaut2_scheme), db :Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "could not validate credential", headers={"WWW-Authenticate": "Bearer"})

    token_data = verify_token(token, credentials_exception)

    current_user = db.query(models.ap).filter(models.ap.name == token_data.user).first()
    return current_user
