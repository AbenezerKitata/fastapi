from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status, HTTPException
from ..dbConnect import get_db
from typing import List
from ..schemas.media import ReturnMedia, CreateMedia
from ..models.media import Media
from ..oauth2 import get_current_user

router = APIRouter(prefix="/media", tags=["Media"])


# Get all
@router.get("/", response_model=List[ReturnMedia])
async def readMedias(db: Session = Depends(get_db)):
    allMedia = db.query(Media).all()
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
    inserted = Media(**payload.model_dump())
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
    if found.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to delete, no item with the id of {id} exists",
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
    update_query.update(updated_data.model_dump(), synchronize_session=False)
    db.commit()
    return "SUCCESS"
