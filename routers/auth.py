from fastapi import HTTPException, Depends, APIRouter, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas, utils, oauth
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(
    tags = ['Authentication']
)


@router.post("/login", response_model= schemas.token)
async def login(credentials: OAuth2PasswordRequestForm =Depends(), db:Session = Depends(get_db)):

    user = db.query(models.ap).filter(models.ap.name == credentials.username).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = "invalid details!")

    if not utils.verifyPwd(credentials.password, user.password) :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = "invalid details!")

    #create_token
    access_token = oauth.create_token({"user": user.name})
    return {"access_token" : access_token, "token_type" : "bearer"}
