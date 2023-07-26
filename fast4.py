from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models
from .database import engine, sessionlocal, get_db
import pydantic
from .routers import users, auth, posts


app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(posts.router)


origins = ['https://www.google.com']

app.add_middleware(CORSMiddleware, allow_origins = origins,
    allow_credentials = True, allow_headers = ['*'], allow_methods = ['*'])

@app.get("/")
async def hello():
    return {"message" : "hello user"}
