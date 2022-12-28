from app.db import session
from app.models import Users
from app.utils import password_hasher

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