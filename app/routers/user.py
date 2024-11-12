from sqlalchemy.orm import Session
from .. import models , schemas
from .. database import engin , get_db
from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter
from passlib.context import CryptContext
from typing import List


router = APIRouter(tags=['user'])






pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engin)



@router.get("/users" , response_model=List[schemas.UserRespond])
async def get_users(db:Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.post("/creatuser" ,status_code=status.HTTP_201_CREATED , response_model=schemas.UserRespond )
async def create_user(user: schemas.UserCreate ,db:Session=Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    new_user= models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/user/{ID}"  ,response_model=schemas.UserRespond )
async def get_user(ID: int,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == ID).first()



    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data for ID {ID} not found"
        )
    
    return user


