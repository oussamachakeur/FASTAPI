from sqlalchemy.orm import Session
from .. import models , schemas , token
from .. database import engin , get_db
from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter
from typing import List


router= APIRouter(tags=['food'])

models.Base.metadata.create_all(bind=engin)


@router.get('/food',response_model=List[schemas.FoodLRespond])

async def get_food(db:Session=Depends(get_db) ,user_id :int = Depends(token.get_current_user) ):
    food = db.query(models.Food).all()
    return food

@router.post('/add food' , response_model=schemas.FoodLRespond , status_code=status.HTTP_201_CREATED)
async def add_food(food:schemas.FoodCreate ,db:Session=Depends(get_db)):
    new_food= models.Food(**food.dict())
    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return new_food

@router.get('/food/{id}' , response_model= schemas.FoodLRespond)
async def food( id: int ,db : Session=Depends(get_db) , user_id :int = Depends(token.get_current_user)):
    food = db.query(models.Food).filter(models.Food.foodID == id).first()
    if food is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"food id {id} not found")
    return food


@router.delete('/food/delete/{id}')
async def delete_food( id: int , db : Session= Depends(get_db) , user_id :int = Depends(token.get_current_user)):
    food_deleted = db.query(models.Food).filter(models.Food.foodID==id).first()
    
    if food_deleted is None :
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND , detail= f"food id {id} not found")
    
    db.delete(food_deleted)
    db.commit()

    return f"the food with id ({id}) is deleted succesfully"

@router.put('/food/update/{id}')
async def food_update(id: int, food: schemas.FoodUpdate, db: Session = Depends(get_db)):
    updated_food = db.query(models.Food).filter(models.Food.foodID == id).first()
    
    if updated_food is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Food ID {id} not found")
    
    for key, value in food.dict().items():
        setattr(updated_food, key, value)
    
    db.commit()
    db.refresh(updated_food)
    
    return {"message": "Data has been updated successfully!", "updated_food": updated_food}
