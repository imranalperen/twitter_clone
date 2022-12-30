from app.db import session
from app.models import Users, Tweets, UsersFollowers
from app.utils import password_hasher
from sqlalchemy.sql import not_, and_
import random

class UserMain:
    def signup(self, name, username, email, password):
        user_username = (
            session.query(Users)
            .filter(Users.username == f"{username}")
            .first()
        )
        if user_username:
            return {"status": False, "message": 1001}

        user_email = (
            session.query(Users)
            .filter(Users.email == f"{email}")
            .first()
        )
        if user_email:
            return {"status": False, "message": 1002}
        
        user = Users(
            name = name,
            username = username,
            email = email,
            hashed_password = password_hasher(password, username)
        )
        session.add(user)
        session.commit()
        return {"status": True}


    def login(self, username, password):
        user_query = (
            session.query(Users)
            .filter(Users.username == f"{username}")
            .first()
        )
        if not user_query:
            return {"status": False, "message": 1001}


        hashed_password = password_hasher(password, username)
        if(user_query.hashed_password != hashed_password):
            return {"status": False, "message": 1003}
        
        return {"status": True}

    
    def update_acces_token(self, username, access_token):
        (
            session.query(Users)
            .filter(Users.username == f"{username}")
            .update({
                "access_token": access_token["token"],
                "access_token_expire_date": access_token["end_date"]
            })
        )
        session.commit()


    def get_user_by_acc_token(self, access_token):
        user = (
            session.query(Users)
            .filter(Users.access_token == f"{access_token}")
            .first()
        )
        if not user:
            return False
        
        return user


    def get_user_follow_list_by_id(self, user_id):
        following_list = (
            session.query(UsersFollowers)
            .filter(UsersFollowers.main_user_id == f"{user_id}")
            .all()
        )
        print(following_list)
        return following_list

    
    def recommend_two_user(self, follow_list, main_user_id):
        if not follow_list:
            recommended_users_temp = (
                session.query(Users)
                .filter(Users.id != f"{main_user_id}")
                .limit(2)
                .all()
            )

        
        recommended_users = {}
        for i in range(2):
            recommended_users[i] = {
                "id": recommended_users_temp[i].id,
                "name": recommended_users_temp[i].name,
                "username": recommended_users_temp[i].username,
                "is_following": False
            }

        return recommended_users

    
    def follow_user(self, main_user, following_user_id):
        query = UsersFollowers(
            main_user_id = main_user.id,
            following_user_id = following_user_id
        )
        session.add(query)
        session.commit()
        return {"status": True}


    def unfollow_user(self, main_user, unfollowing_user_id):
        query = UsersFollowers(
            main_user_id = main_user.id,
            following_user_id = unfollowing_user_id
        )
        session.delete(query)
        session.commit()

        return {"status": True}



class TweetMain:
    def add_tweet(self, user, tweet_body):
        if(len(tweet_body) > 280 or len(tweet_body) < 1):
            return {"status": False, "message": 2001}
        
        tweet = Tweets(user_id = user.id, body = tweet_body)
        session.add(tweet)
        session.commit()
        return {"status": True}