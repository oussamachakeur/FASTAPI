from .database import Base
from sqlalchemy import * 
from sqlalchemy.sql.expression import  null 
  

class Food(Base):
    __tablename__= "food"
    foodID = Column(Integer, primary_key=True, autoincrement=True)
    foodname = Column(String(50), nullable=False)
    weight = Column(Float, nullable=True)
    calories = Column(Float, nullable=True)
    eat_time = Column(Time, default=func.current_time())
    sign_up_date = Column(Date, default=func.current_date())

class User(Base):
    __tablename__ = "clients"
    userID = Column(Integer, Sequence("users_seq", start=100000), primary_key=True)
    FirstName = Column(String(50), nullable=False)
    LastName = Column(String(50), nullable=False)
    Age = Column(Integer, nullable=False)
    height = Column(DECIMAL(5, 2),  nullable=False)
    weight = Column(DECIMAL(5, 2), nullable=False)
    Gender = Column(String(10), nullable=True)  
    bodyFatPercentage = Column(DECIMAL(5, 2), nullable=True)
    goal = Column(String(20), nullable=True)
    activity_level = Column(String(30), nullable=True)
    email = Column(String(40), unique=True, nullable=False)
    passwords = Column(String, nullable=False)
    sign_up_date = Column(Date, default=func.current_date())
    last_login = Column(TIMESTAMP, default=func.current_timestamp())




class Exercice(Base):
    __tablename__ = "exercice"
    
    exerciceID = Column(Integer, primary_key=True, autoincrement=True)
    exercicename = Column(String(50), nullable=False)
    weight = Column(Float, CheckConstraint("weight >= 0"), nullable=True)
    reps_number = Column(Integer, CheckConstraint("reps_number > 0"), nullable=False)
    sets_number = Column(Integer, CheckConstraint("sets_number > 0"), nullable=False)
    between_reps_time = Column(Float, CheckConstraint("between_reps_time >= 0"), nullable=True)
    between_sets_time = Column(Float, CheckConstraint("between_sets_time >= 0"), nullable=True)
    training_time = Column(Time, default=func.current_time())
    training_date = Column(Date, default=func.current_date())
