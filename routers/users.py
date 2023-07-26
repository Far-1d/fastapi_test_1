from fastapi import Depends, APIRouter, status
from .. import models, schemas, utils
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session


router = APIRouter(
    prefix = "/users",
    tags = ['users']
)


@router.get("/", status_code=status.HTTP_200_OK, response_model =List[schemas.users_out] )
async def get_users(db:Session = Depends(get_db)):

    users = db.query(models.ap).all()
    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model =schemas.users_out)
async def create_users(users:schemas.user, db:Session = Depends(get_db)):

    users.password = utils.hashPwd(users.password)

    new_user = models.ap(**users.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
