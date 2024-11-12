from pydantic import BaseModel , EmailStr
from typing import Optional




class UserRespond(BaseModel):
    email: str
    class Config:
        orm_mode  = True



class UserCreate(BaseModel):
    email : EmailStr
    password : str

    
class UserLogin(BaseModel):
    email: EmailStr
    password: str






class PostUpdate(BaseModel):
    title: str
    content: str

class PostCreate(PostUpdate):
    title: str
    content: str
    #here below i put 2024 because its optional field , if the user didnt enter a year , then automatecally will be 2024
    year:int=2024

class PostRespond(BaseModel):
    title: str
    content :str
    user_id: int
    user :UserRespond

    class Config:

        orm_mode  = True

class Voteout(BaseModel):
    title: str
    content :str
    user_id: int
    user :UserRespond
    Vote:int
    
    class config:
        orm_mode  = True




class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str]= None
    
    
##############vote ################


class Vote(BaseModel):
    post_id : int 
    like : int








