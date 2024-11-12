from sqlalchemy.orm import Session
from .. import models , schemas
from .. database import engin , get_db
from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter
from typing import List
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=['users'])

# Use Base.metadata to create tables
models.Base.metadata.create_all(bind=engin)

@router.get("/users" , response_model=List[schemas.PostRespond])
async def get_users(db:Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.post("/creatuser" ,status_code=status.HTTP_201_CREATED , response_model=schemas.PostRespond )
async def create_user(user: schemas.CreateUser ,db:Session=Depends(get_db)):
    hashed_password = pwd_context.hash(user.passwords)
    user.passwords = hashed_password
    new_user= models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/user/{ID}"  ,response_model=schemas.PostRespond )
async def get_user(ID: int,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.userID == ID).first()


    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data for ID {ID} not found"
        )
    
    return user

@router.delete("/user/delete/{ID}")
async def delete_user(ID: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.userID == ID).first()
    
    if user is None:  # Corrected this line
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data for ID {ID} not found"
        )
    
    db.delete(user)  # Use db.delete instead of post.delete
    db.commit()

    return {"message": "user has been deleted"}


@router.put("/user/update/{ID}" ,response_model=schemas.PostRespond)  
async def update_user(ID: int, user: schemas.UpdateUser, db: Session = Depends(get_db)):  # Include db session
    existing_post = db.query(models.User).filter(models.User.userID == ID).first()
    
    if existing_post is None:  # Check if the post exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data for ID {ID} not found"
        )
    for key, value in user.dict().items():
        setattr(existing_post, key, value) 
    db.commit()  # Commit changes to the database
    db.refresh(existing_post)  # Refresh the instance with the new data

    return existing_post  # Return the updated post

 
 
