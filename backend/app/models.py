from app.db import Base, engine
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean
)
from sqlalchemy.sql import func

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    username = Column(String(15), nullable=False, unique=True)
    email = Column(String(30), nullable=False, unique=True)
    hashed_password = Column(String(100), nullable=False)
    access_token = Column(String(100))
    access_token_expire_date = Column(DateTime)



Base.metadata.create_all(engine)