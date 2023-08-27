from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from ..dbConnect import Base
from sqlalchemy.sql.expression import text


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    # firstName = Column(String, nullable=False)
    # lastName = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
