from app.db import session
from app.models import Users, UsersFollowers
from app.utils import password_hasher
from sqlalchemy.sql import and_

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