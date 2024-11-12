from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .Config import settings
 


database_url = settings.DB_url
engin = create_engine(database_url)
sessionlocal = sessionmaker(autoflush= False , autocommit = False , bind= engin)
Base = declarative_base()

def get_db():
    db= sessionlocal()
    try:
        yield db
    finally:
        db.close()