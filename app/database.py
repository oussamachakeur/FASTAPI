from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Create the database URL using the settings
database_url = settings.DB_URL

# Set up the database engine and sessionmaker (remove connect_args for PostgreSQL)
engin = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engin)

# Base class for the models
Base = declarative_base()

# Dependency to get the database session in your application
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
