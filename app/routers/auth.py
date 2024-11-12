from fastapi import FastAPI , Response , status , HTTPException , Depends ,APIRouter
from .. import database , schemas , models , password_hash , oauth2
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=['authentication'] )


@router.post('/login', status_code=status.HTTP_201_CREATED , response_model= schemas.Token)
def login(user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.username).first()
    if user  is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="invalid data"
        )
    
    if not password_hash.verify(user_data.password , user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="invalid data"
        )

    #create token
    access_token = oauth2.create_access_token(data={"user_id":user.id})

    return {"access_token": access_token, "token_type": "bearer"}




    
    







 