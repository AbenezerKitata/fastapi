from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from ..dbConnect import Base
from sqlalchemy.sql.expression import text


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    cool = Column(Boolean, server_default="TRUE", nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
