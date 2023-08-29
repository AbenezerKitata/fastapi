from operator import and_
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status, HTTPException
from ..dbConnect import get_db
from typing import List, Optional
from ..schemas.media import ReturnMedia, CreateMedia
from ..models.media import Media
from ..oauth2 import get_current_user

router = APIRouter(prefix="/media", tags=["Media"])


# Get all
@router.get("/", response_model=List[ReturnMedia])
async def readMedias(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
    limit: int = 5,
    skip: int = 0,
    title: Optional[str] = "",
):
    # For social media
    # allMedia = db.query(Media).all()
    # For Note taking/ more private apps
    allMedia = (
        db.query(Media)
        .filter(and_(Media.title.contains(title), Media.owner_id == current_user.id))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return allMedia


# Get one
@router.get("/{id}", response_model=ReturnMedia)
async def getMedia(id: int, db: Session = Depends(get_db)):
    found = db.query(Media).filter(Media.id == id).first()

    if found == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Media with an id of {id} not found",
        )

    return found


# Create
@router.post("/", response_model=ReturnMedia)
async def createMedia(
    payload: CreateMedia,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    print(current_user.email)
    inserted = Media(owner_id=current_user.id, **payload.model_dump())
    db.add(inserted)
    db.commit()
    db.refresh(inserted)
    return inserted


# Delete
@router.delete("/{id}")
async def deleteMedia(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    found = db.query(Media).filter(Media.id == id)
    foundFirst = found.first()
    if foundFirst == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to delete, no item with the id of {id} exists",
        )
    # authorization
    if foundFirst.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to do this action",
        )
    found.delete(synchronize_session=False)
    db.commit()
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
    )


# Update
@router.put("/{id}", response_model=ReturnMedia)
async def updateMedia(
    id: int,
    updated_data: CreateMedia,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    update_query = db.query(Media).filter(Media.id == id)
    updated_itm = update_query.first()
    if updated_itm == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No item with the id of {id} exists",
        )
        # authorization
    if updated_itm.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to do this action",
        )
    update_query.update(updated_data.model_dump(), synchronize_session=False)
    db.commit()
    return updated_itm
