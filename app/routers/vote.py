from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..schemas.vote import ReturnVote
from ..dbConnect import get_db
from ..oauth2 import get_current_user
from ..models.votes import Vote
from ..models.media import Media


router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: ReturnVote,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    media = db.query(Media).filter(Media.id == vote.media_id).first()
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Media with id: {vote.media_id} doesnt exist!",
        )

    vote_query = db.query(Vote).filter(
        Vote.media_id == vote.media_id, Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if vote.direction == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{current_user.id} has already voted on media {vote.media_id}",
            )
        new_vote = Vote(media_id=vote.media_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully saved vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
