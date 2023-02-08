from app.db import session
from app.models import Users, UsersFollowers, VerificationCodes, Notificatons, Tweets
from app.utils import password_hasher
from sqlalchemy.sql import and_
from config import UPLOAD_FOLDER_URL
from datetime import datetime


class UserMain:
    def get_profile_image_by_username(self, username):
        q = (
            session.query(Users)
            .where(Users.username == username)
            .first()
        )
        profile_image = q.profile_image
        return profile_image

    def get_user_by_username(self, username):
        q = (
            session.query(Users)
            .where(Users.username == username)
            .first()
        )
        user = []
        user.append({
            "id": q.id,
            "name": q.name,
            "username": q.username,
            "profile_image": q.profile_image,
        })
        return user
    
    def get_user_query_by_username(self, username):
        user = (
            session.query(Users)
            .where(Users.username == username)
            .first()
        )
        return user
    

    def user_notifications(self, user_id):
        q = (
            session.query(Notificatons)
            .where(Notificatons.target_user_id == user_id)
            .order_by(Notificatons.date.desc())
            .limit(40)
            .all()
        )
        notifications_list = []
        if q:
            for i in q:
                user_query = (
                    session.query(Users)
                    .where(Users.id == i.user_id)
                    .first()
                )
                tweet_query = (
                    session.query(Tweets)
                    .where(Tweets.id == i.tweet_id)
                    .first()
                )
                date_now = str(datetime.now())
                notifications_list.append({
                    "user_id": user_query.id,
                    "name": user_query.name,
                    "username": user_query.username,
                    "profile_image": user_query.profile_image,
                    "tweet_id": tweet_query.id,
                    "tweet_body": tweet_query.body,
                    "tweet_image": tweet_query.image,
                    "date": date_now,
                    "event": i.event
                })
        return notifications_list

    def notifications_count(self, user_id):
        q = (
            session.query(Notificatons)
            .where(and_(
                Notificatons.target_user_id == user_id,
                Notificatons.is_readed == False
            ))
            .count()
        )
        return q
    
    def mark_as_read_notifications(self, user_id):
        q = (
            session.query(Notificatons)
            .where(and_(
                Notificatons.target_user_id == user_id,
                Notificatons.is_readed == False
            ))
            .all()
        )
        if q:
            (
                session.query(Notificatons)
                .where(Notificatons.is_readed == False)
                .update({
                    "is_readed": True
                })
            )
            session.commit()

    def search_users(self, keyword):
        # Post.query.filter(Post.tags.like(search)).all()
        q = (
            session.query(Users)
            .where(Users.username.like(keyword))
            .all()
        )
        users = []
        for i in q:
            users.append({
                "id": i.id,
                "username":i.username,
                "name": i.name,
                "profile_image": i.profile_image,
            })
        return users




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
    

    def update_user_profile_image(self, user, profile_image, bio):
        if profile_image:
            user.profile_image = UPLOAD_FOLDER_URL + profile_image
        if bio:
            user.biography = bio
        session.commit()

    def edit_user_profile(self, user, image, name, bio):
        if image:
            user.profile_image = UPLOAD_FOLDER_URL + image
        if name:
            user.name = name
        user.biography = bio
        session.commit()
    
    def get_user_by_mail(self, mail):
        q = (
            session.query(Users)
            .where(Users.email == mail)
            .first()
        )
        if q:
            return q
        return False
    
    def save_verfication_code(self, user, verification_code):
        #if there is an verification code in db we will update
        #if not we will create
        q = (
            session.query(VerificationCodes)
            .where(VerificationCodes.user_id == user.id)
            .first()
        )
        if q:
            (
                session.query(VerificationCodes)
                .where(VerificationCodes.user_id == user.id)
                .update({
                    "verification_code": verification_code
                })
            )
            session.commit()
        else:
            q = VerificationCodes(
                user_id = user.id,
                verification_code = verification_code
            )
            session.add(q)
            session.commit()
        
    def compare_verification_codes(self, user, verify_code):
        q = (
            session.query(VerificationCodes)
            .where(VerificationCodes.user_id == user.id)
            .first()
        )
        verify_code = int(verify_code)
        if verify_code == q.verification_code:
            return True
        return False
    
    def update_user_password(self, user, password):
        hashed_password = password_hasher(password, user.username)
        (
            session.query(Users)
            .where(Users.id == user.id)
            .update({
                "hashed_password": hashed_password,
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

    def get_user_follows_or_followers(self, visit_user_id, purpose, user_id):
        users = []
        if purpose == "follows":
            #return followers of user
            users_query = (
                session.query(Users)
                .join(UsersFollowers, UsersFollowers.following_user_id == Users.id)
                .where(UsersFollowers.main_user_id == visit_user_id)
                .all()
            )

            if users_query:
                for user in users_query:
                    is_following_query = (
                        session.query(UsersFollowers)
                        .where(and_(
                            UsersFollowers.following_user_id == user.id,
                            UsersFollowers.main_user_id == user_id
                        ))
                        .first()
                    )
                    is_following = False
                    if is_following_query:
                        is_following = True

                    users.append({
                        "id": user.id,
                        "name": user.name,
                        "username": user.username,
                        "image": user.profile_image,
                        "is_following": is_following
                    })

        if purpose == "followers":
            #return follows of user
            users_query = (
            session.query(Users)
            .join(UsersFollowers, UsersFollowers.main_user_id == Users.id)
            .where(UsersFollowers.following_user_id == visit_user_id)
            .all()
            )

            if users_query:
                for user in users_query:
                    is_following_query = (
                        session.query(UsersFollowers)
                        .where(and_(
                            UsersFollowers.following_user_id == user.id,
                            UsersFollowers.main_user_id == user_id
                        ))
                        .first()
                    )
                    is_following = False
                    if is_following_query:
                        is_following = True
                    
                    users.append({
                        "id": user.id,
                        "name": user.name,
                        "username": user.username,
                        "image": user.profile_image,
                        "is_following": is_following
                    })
        
        return users