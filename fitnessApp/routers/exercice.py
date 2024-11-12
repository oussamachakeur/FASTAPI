from sqlalchemy.orm import Session
from .. import models , schemas , token
from .. database import engin , get_db
from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter
from typing import List


router = APIRouter(tags=['exercice'])

models.Base.metadata.create_all(bind=engin)



@router.get('/exercices' , response_model =List[schemas.ExerciceRespond])
async def get_exercices(db : Session=Depends(get_db) ,user_id :int = Depends(token.get_current_user)):
    exercices = db.query(models.Exercice).all()
    return exercices

@router.post('/add exercice' )
async def add_exercice(exercice: schemas.ExerciceCreate , db :Session=Depends(get_db) ):
    new_exercice= models.Exercice(**exercice.dict())
    db.add(new_exercice)
    db.commit()
    db.refresh(new_exercice)
    return "exercice has been added succesfully"

@router.get('/exercices/{id}' , response_model=schemas.ExerciceRespond)
async def one_exercice(id: int , db :Session=Depends(get_db)):
    exercice = db.query(models.Exercice).filter(models.Exercice.exerciceID == id).first()
    if exercice is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f" exercice with id ({id}) is not found")
    return exercice

@router.delete('/exercices/delete/{id}' )
async def delete_exercice(id :int , db :Session = Depends(get_db)):
    deleted_ex = db.query(models.Exercice).filter(models.Exercice.exerciceID == id).first()
    if deleted_ex is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f" exercice with id ({id}) is not found")
    db.delete(deleted_ex)
    db.commit()

    return f"exercice with id ({id}) is deleted"

@router.put('/exercices/update/{id}')
async def ex_update( id:int , exercice: schemas.ExerciceUpdate , db : Session= Depends(get_db)):
    updated_ex = db.query(models.Exercice).filter(models.Exercice.exerciceID == id).first()
    if updated_ex is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f" exercice with id ({id}) is not found")
    for key , values in exercice.dict().items():
        setattr(updated_ex , key , values)

    db.commit()
    db.refresh(updated_ex)

    return f"exercice with id ({id}) is updated"
    



