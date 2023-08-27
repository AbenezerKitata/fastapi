from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from .. import utils
from ..models.user import User
from sqlalchemy.exc import IntegrityError
from ..dbConnect import get_db
from ..schemas.user import CreateUser, ReturnUser

router = APIRouter(prefix="/user", tags=["Users"])


# Create
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReturnUser)
async def createUser(payload: CreateUser, db: Session = Depends(get_db)):
    try:
        # hash the pw
        payload.password = utils.hash(payload.password)
        inserted = User(**payload.model_dump())
        db.add(inserted)
        db.commit()
        db.refresh(inserted)
        return inserted
    except IntegrityError as e:
        db.rollback()  # Roll back the transaction to avoid partial insertion
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the same data already exists",
        )


# Get One
@router.get("/{id}", response_model=ReturnUser)
async def getUser(id: int, db: Session = Depends(get_db)):
    found = db.query(User).filter(User.id == id).first()

    if found == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with an id of {id} not found",
        )

    return found
