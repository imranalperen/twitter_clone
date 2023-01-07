from app.db import Base, engine
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    username = Column(String(15), nullable=False, unique=True)
    email = Column(String(30), nullable=False, unique=True)
    hashed_password = Column(String(100), nullable=False)
    profile_image = Column(String)
    date_of_birth = Column(String(30))
    gender = Column(String(10))
    verified_accaunt = Column(Boolean, default=False)
    access_token = Column(String(100))
    access_token_expire_date = Column(DateTime)


class Tweets(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id") ,nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    body = Column(String(280))
    image = Column(String)


class UsersFollowers(Base):
    __tablename__ = "users_followers"

    id = Column(Integer, primary_key=True)
    main_user_id = Column(Integer, ForeignKey("users.id"))
    following_user_id = Column(Integer, ForeignKey("users.id"))


Base.metadata.create_all(engine)