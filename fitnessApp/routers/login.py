from fastapi import FastAPI , Response , status , HTTPException , Depends ,APIRouter
from .. import database , schemas , models , password_hash , token
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router = APIRouter(tags=['login'])


@router.post('/login', status_code=status.HTTP_201_CREATED, response_model=schemas.Token)
async def login(user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not password_hash.verify(user_data.password, user.passwords):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    token_access = token.create_access_token(data={'userID': user.userID})  # Adjust if needed
    
    return {"token_access": token_access, "token_type": "bearer"}  # Ensure this matches your response model


