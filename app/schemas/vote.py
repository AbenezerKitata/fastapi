from pydantic import BaseModel, conint
from datetime import datetime


class ReturnVote(BaseModel):
    media_id: int
    direction: conint(ge=0, le=1)
