from pydantic import BaseModel
from datetime import datetime
from typing import List
from uuid import UUID

class users_out (BaseModel):
    name : str
    time : datetime
    items : List
    class Config:
        orm_mode = True


class login (BaseModel):
    name: str
    password : str


class creator (BaseModel):
    name:str
    class Config:
        orm_mode = True

class user (login):
    items : List = []


class token (BaseModel):
    access_token: str
    token_type : str


class payload (BaseModel):
    user:str



class post(BaseModel):
    title :str
    content :str



class post_out(post):
    created_at :datetime
    owner : creator
    class Config:
        orm_mode = True

class post_all(post):
    created_at : datetime
    name : str
    class Config:
        orm_mode = True
