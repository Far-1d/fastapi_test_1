from fastapi import Depends, APIRouter, status, HTTPException
from .. import models, schemas, utils,oauth
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session, join


router = APIRouter(
    prefix = "/posts",
    tags = ['posts']
)


@router.get("/", status_code=status.HTTP_200_OK, response_model= List[schemas.post_out])
async def get_posts(db:Session = Depends(get_db)):

    posts = db.query(models.post).all()
    return posts


#@router.get("/{id}", status_code=status.HTTP_200_OK, response_model =schemas.post_all)
#async def get_post(id:str, db:Session = Depends(get_db), user:str =Depends(oauth.get_current_user)):

#    db.query(models.post).join(models.ap)
#    return


@router.post("/", status_code=status.HTTP_201_CREATED, response_model =schemas.post_out)
async def create_posts(posts:schemas.post, db:Session = Depends(get_db),
        user:str =Depends(oauth.get_current_user)):


    dict_post = posts.dict()
    dict_post.update({"user_id": str(user.id)})

    new_post = models.post(**dict_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:str, db:Session = Depends(get_db),
        user:str =Depends(oauth.get_current_user)):

        query = db.query(models.post).filter(models.post.id == id)
        
        if query.first() == None :
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND
                                , detail= f"post with id: {id} not found")

        if query.first().user_id != user.id :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                detail="you are not authorized to do such action!")

        query.delete(synchronize_session=False)
        db.commit()
