from app.db import session
from app.models import Users, UsersFollowers
from app.utils import password_hasher
from sqlalchemy.sql import and_
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
                "is_following": False
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

 