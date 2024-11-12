from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

router = APIRouter(tags=['votes'])

@router.post("/vote", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Check if the user has already liked the post
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if vote.like == 1:
        # If the vote already exists, raise an exception to avoid duplicates
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="post already liked")
        
        # Otherwise, add a new vote
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "post has been liked successfully"}
    
    elif vote.like == 0:
        # If no vote is found, raise an exception indicating the post is not liked
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        
        # Otherwise, delete the vote
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "like has been removed"}
