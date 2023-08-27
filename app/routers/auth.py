from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..dbConnect import get_db
from ..schemas.auth import Token
from ..models.user import User as userModel
from ..utils import verify
from ..oauth2 import create_access_token


router = APIRouter(prefix="/login", tags=["Auth"])


@router.post("/", response_model=Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    foundUser = (
        db.query(userModel).filter(userModel.email == user_credentials.username).first()
    )
    if not foundUser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect email/password combination",
        )
    if not verify(user_credentials.password, foundUser.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect email/password combination",
        )
    access_token = create_access_token(data={"user_id": foundUser.id})
    return {"access_token": access_token, "token_type": "bearer"}
