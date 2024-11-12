from fastapi import FastAPI
import psycopg2 
from psycopg2.extras import RealDictCursor
from .database import engin , get_db
from . import models 
from .models import Base
from sqlalchemy.orm import session
from .routers import users , food ,exercice , login
from passlib.context import CryptContext
from .Config import settings




pwd_context= CryptContext(schemes=['bcrypt'] , deprecated=['auto'])
models.Base.metadata.create_all(engin)

app = FastAPI()



try:
    conn = psycopg2.connect (host='localhost' , database='fitness app' , user = 'postgres', password='kaddakadda' , cursor_factory= RealDictCursor)
    cursor = conn.cursor()
    print("we are connected to the database succesfully")
except:
    print("connecting to the database is failed")







app.include_router(users.router)
app.include_router(food.router)
app.include_router(exercice.router)
app.include_router(login.router)