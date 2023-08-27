from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


class MediaBase(BaseModel):
    title: str
    content: str
    cool: bool
    rating: int


class CreateMedia(MediaBase):
    pass


class ReturnMedia(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    created_at: datetime
