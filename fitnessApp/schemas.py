from pydantic import BaseModel, EmailStr, constr, condecimal
from typing import Optional
from datetime import date, datetime





class PostRespond(BaseModel):
    LastName : str
    email :str

    class config:
        orm_mode = True

class CreateUser(BaseModel):
    FirstName: str
    LastName: str
    Age: int
    height: float # Height must be greater than 0
    weight: float  # Weight must be greater than 0
    Gender: str  # Gender can be 'Male' or 'Female'
    bodyFatPercentage: float  # Between 0 and 100
    goal: str  # Goal must be one of the specified options
    email: EmailStr  # Valid email format
    passwords: str  # Assuming password is a string
    sign_up_date: Optional[date] = None  # Default to None if not provided
    last_login: Optional[datetime] = None  # Default to None if not provided

class UpdateUser(BaseModel):
    password: str
    Age : int
    height: float
    weight: float
    goal : str
#############################food#########################

class FoodLRespond(BaseModel):
    foodID : int
    foodname : str
    weight: float
    calories:float


    class config:
        orm_mode = True


class FoodCreate(BaseModel):
    foodname : str
    weight: float
    calories:float
    eat_time : Optional[date] = None  
    sign_up_date: Optional[datetime] = None 

class FoodUpdate(BaseModel):
    foodname : str
    weight: float


###################exercices##########################

class ExerciceRespond(BaseModel):
    exercicename: str
    weight:float
    reps_number: int
    sets_number : int
    between_reps_time: float
    between_sets_time : float

    class config:
        orm_mode= True

class ExerciceCreate(BaseModel):
    exercicename: str
    weight:float
    reps_number: int
    sets_number : int
    between_reps_time: float
    between_sets_time : float

class ExerciceUpdate(BaseModel):
    exercicename: str
    weight:float
    reps_number: int
    sets_number : int
    between_reps_time: float
    between_sets_time : float

################# token ##########################

class Token(BaseModel):
    token_access :str 
    token_type : str

class TokenData(BaseModel):
    id : Optional[str] = None
