from typing import List
from fastapi import FastAPI , Response , status , HTTPException , Depends
from fastapi.params import Body
from pydantic import BaseModel 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models , schemas
from .database import engin, get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .routers import post , user , auth , vote



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engin)


app = FastAPI()

 




try:
    conn= psycopg2.connect(host='localhost',database='school' , user='postgres' , password="kaddakadda" , cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('we connected to the database succsesfully')
except:
    print("connecting is failed")




app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

















    