from app.db import session
from app.models import Users, UsersFollowers, Tweets
from app.utils import password_hasher
from sqlalchemy.sql import and_, label, union, subquery
from sqlalchemy import func

class UserRegistration:
    def signup(self, name, username, email, password):
        user_username = (
            session.query(Users)
            .where(Users.username == f"{username}")
            .first()
        )
        if user_username:
            return {"status": False, "error": 1001}

        user_email = (
            session.query(Users)
            .where(Users.email == f"{email}")
            .first()
        )
        if user_email:
            return {"status": False, "error": 1002}
        
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
            .where(Users.username == f"{username}")
            .first()
        )
        if not user_query:
            return {"status": False, "error": 1001}


        hashed_password = password_hasher(password, username)
        if(user_query.hashed_password != hashed_password):
            return {"status": False, "error": 1003}
        
        return {"status": True}

    
    def update_acces_token(self, username, access_token):
        (
            session.query(Users)
            .where(Users.username == f"{username}")
            .update({
                "access_token": access_token["token"],
                "access_token_expire_date": access_token["end_date"]
            })
        )
        session.commit()


    def get_user_by_acc_token(self, access_token):
        user = (
            session.query(Users)
            .where(Users.access_token == f"{access_token}")
            .first()
        )
        if not user:
            return False
        
        return user
    

    def update_user_info(self, user, image, date_of_birth, gender):
        if(gender and date_of_birth):
            (
                session.query(Users)
                .where(Users.id == user.id)
                .update({
                    "profile_image": image,
                    "date_of_birth": date_of_birth,
                    "gender": gender
                })
            )
        else:
            (
                session.query(Users)
                .where(Users.id == user.id)
                .update({
                    "profile_image": image
                })
            )
        session.commit()


class UserFollow:
    def recommend_two_user(self, main_user_id):       
        query = (
            session.query(Users)
            .outerjoin(UsersFollowers, and_(
                UsersFollowers.following_user_id==Users.id,
                UsersFollowers.main_user_id==main_user_id
                )
            )
            .where(UsersFollowers.id==None)
            .where(Users.id!=main_user_id)
            .order_by(func.random())
            .limit(2)
            .all()
        )
        # from sqlalchemy.dialects import postgresql
        # x = str(q.statement.compile(dialect=postgresql.dialect()))
        recommended_users = []
        for user in query:
            recommended_users.append({
                "id": user.id,
                "name": user.name,
                "username": user.username,
                "is_following": False,
                "image": user.profile_image
            })

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
        (
            session.query(UsersFollowers)
            .where(and_(
                UsersFollowers.main_user_id == f"{main_user.id}",
                UsersFollowers.following_user_id == f"{unfollowing_user_id}"
            ))
            .delete()
        )
        session.commit()

        return {"status": True}


class UserMain:
    def create_timeline(self, user):
        #raw sql
        # select (
        #     users.id,
        #        users.name,
        #        users.username,
        #        tweets.time_created,
        #        tweets.body
        #            ) from users
        # inner join tweets on tweets.user_id = users.id
        # inner join users_followers on users_followers.following_user_id = users.id
        # where users_followers.main_user_id = 4
        # union
        # select (
        #     users.id,
        #        users.name,
        #        users.username,
        #        tweets.time_created,
        #        tweets.body
        #            ) from users
        # inner join tweets on tweets.user_id = users.id
        # inner join users_followers on users_followers.main_user_id = users.id
        # where users_followers.main_user_id = 4

        #tweets of following users
        q1 = (
            session.query(
                Users.id,
                Users.name,
                Users.username,
                Tweets.time_created,
                Tweets.body,
                Tweets.id.label("tweet_id"),
                Tweets.image
            )
            .join(Tweets, Tweets.user_id == Users.id)
            .join(UsersFollowers, UsersFollowers.following_user_id == Users.id)
            .where(UsersFollowers.main_user_id == user.id)
            
        )
        #tweets of main user
        q2 = (
            session.query(
                Users.id,
                Users.name,
                Users.username,
                Tweets.time_created,
                Tweets.body,
                Tweets.id.label("tweet_id"),
                Tweets.image
            )
            .join(Tweets, Tweets.user_id == Users.id)
            .join(UsersFollowers, UsersFollowers.main_user_id == Users.id)
            .where(UsersFollowers.main_user_id == user.id)
            
        )
        #mergeing 2 queries and sort results descending tweet create time
        q = q1.union(q2).order_by(Tweets.time_created.desc()).all()
        if not q:
            return {"status": False, "error": 2002}

        tweets = []
        for tweet in q:
            tweets.append({
                "tweet_id": tweet.tweet_id,
                "user_id": tweet.id,
                "name": tweet.name,
                "username": tweet.username,
                "time_created": tweet.time_created,
                "body": tweet.body,
                "image": tweet.image
            })
        
        return {"status": True, "tweets": tweets}