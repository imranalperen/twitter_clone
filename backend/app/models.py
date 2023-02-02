from app.db import Base, engine
from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean
)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    username = Column(String(15), nullable=False, unique=True)
    email = Column(String(30), nullable=False, unique=True)
    hashed_password = Column(String(100), nullable=False)
    profile_image = Column(String)
    biography = Column(String(160))
    access_token = Column(String(100))
    access_token_expire_date = Column(DateTime)


class Tweets(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id") ,nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    body = Column(String(280))
    image = Column(String)
    replied_to = Column(Integer)
    is_deleted = Column(Boolean, default=False)


class UsersFollowers(Base):
    __tablename__ = "users_followers"

    id = Column(Integer, primary_key=True)
    main_user_id = Column(Integer, ForeignKey("users.id"))
    following_user_id = Column(Integer, ForeignKey("users.id"))


class TweetsLikes(Base):
    __tablename__ = "tweets_likes"

    id = Column(Integer, primary_key=True)
    tweet_id = Column(Integer, ForeignKey("tweets.id"))
    like_user_id = Column(Integer, ForeignKey("users.id"))
    like_date = Column(DateTime(timezone=True), server_default=func.now())


class Retweets(Base):
    __tablename__ = "retweets"

    id = Column(Integer, primary_key=True)
    tweet_id = Column(Integer, ForeignKey("tweets.id"))
    rt_user_id = Column(Integer, ForeignKey("users.id"))


class Tags(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    tweet_id = Column(Integer, ForeignKey("tweets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    tag_vocab = Column(String, nullable=False)


class VerificationCodes(Base):
    __tablename__ = "verification_codes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    verification_code = Column(Integer)


class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String(500), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    chat_id = Column(Integer, ForeignKey("messages.id"))

class MessageContacts(Base):
    __tablename__ = "message_contacts"

    id = Column(Integer, primary_key=True)
    user_a_id = Column(Integer, ForeignKey("users.id"))
    user_b_id = Column(Integer, ForeignKey("users.id"))

Base.metadata.create_all(engine)