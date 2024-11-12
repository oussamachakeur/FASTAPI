from typing import List , Optional
from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from .. import models , schemas , oauth2
from ..database import engin , get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy import func


router= APIRouter(tags=['post'])

#@router.get("/posts" , response_model= list[schemas.PostRespond])
@router.get("/posts", response_model=List[schemas.Voteout])
async def get_data(
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10, skip: int = 0, search: Optional[str] = ""
):
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("vote"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .limit(limit)
        .offset(skip)
        .all()
    )

    # Map results to response model
    response_data = [
        schemas.Voteout(
            title=result[0].title,
            content=result[0].content,
            user_id=result[0].user_id,
            user=schemas.UserRespond(email=result[0].user.email),
            Vote=result[1]
        )
        for result in results
    ]
    return response_data






@router.post("/ceatePost",status_code=status.HTTP_201_CREATED , response_model=schemas.PostRespond )
async def creat_post(post: schemas.PostCreate ,db:Session=Depends(get_db) , current_user :int = Depends(oauth2.get_current_user) ):
    #cursor.execute("""INSERT INTO posts(title,content,year) VALUES(%s ,%s ,%s)
     #              RETURNING *""" , (post.title , post.content , post.year))
    #new_post = cursor.fetchone()
    #conn.commit()
    #new_post = models.Post(title=post.title , content= post.content , year = post.year)
    new_post= models.Post(user_id=current_user.id,**post.dict())
    db.add(new_post) 
    db.commit()
    db.refresh(new_post)
    return new_post


## imagine we have 15 column in the table , it will be hard to type everytime post.title , post ... ecr , so ther  is a method that we can surely only add ** and dict 



@router.get("/post/{ID}", response_model=schemas.Voteout)
async def get_post(
    ID: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    # Query the post with a join on the Vote model to count votes
    result = (
        db.query(models.Post, func.count(models.Vote.post_id).label("vote"))
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
        .filter(models.Post.id == ID)
        .group_by(models.Post.id)
        .first()
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data for ID {ID} not found"
        )

    post = result[0]
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Action is not allowed for this user"
        )

    # Map the result to the response model
    response_data = schemas.Voteout(
        title=post.title,
        content=post.content,
        user_id=post.user_id,
        user=schemas.UserRespond(email=post.user.email),
        Vote=result[1]  # Count of votes
    )

    return response_data



#@app.delete("/post/delete/{ID}")
#async def delete_post(ID:int):
    cursor.execute("""DELETE  FROM posts WHERE "ID" = %s""", (ID,))
    conn.commit()
    if delete_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data for ID {ID} not found"
        )
    
    return {"data fetched": "data has been deleted"}
@router.delete("/post/delete/{ID}")
async def delete_post(ID: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == ID)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data for ID {ID} not found"
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Action is not allowed for this user"
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Data has been deleted"}





#@app.put("/post/update/{ID}")  # Use the same parameter name in the route and function
#async def update_post(ID: int, post: Post):  # Ensure Post is defined
    cursor.execute("""UPDATE posts SET title = %s, content = %s, year = %s WHERE "ID" = %s RETURNING *""", (post.title, post.content, post.year, ID))
    update_post = cursor.fetchone()
    conn.commit()
    
    if update_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data for ID {ID} not found"
        )
    
    return {"data": update_post}

@router.put("/post/update/{ID}", response_model=schemas.PostRespond)
async def update_post(ID: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    existing_post = db.query(models.Post).filter(models.Post.id == ID).first()
    
    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data for ID {ID} not found"
        )

    if existing_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action is not allowed for this user")
    
    # Update fields with dict unpacking
    for key, value in post.dict().items():
        setattr(existing_post, key, value)
    db.commit()
    db.refresh(existing_post)


    return existing_post

    #existing_post.title = post.title
    #existing_post.content = post.content
    #existing_post.year = post.year   @instead of changing all by one , especially if we have more colimn i would do the dict 