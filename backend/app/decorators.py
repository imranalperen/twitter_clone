from flask import request, jsonify, g
from app.crud.users_crud import UserRegistration, UserMain
from functools import wraps
from datetime import datetime

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get("access-token")
        if not access_token:
            return jsonify({"response": 401})

        user = UserRegistration().get_user_by_acc_token(access_token)
        if not user:
            return jsonify({"response": 401})

        #checking access token expire date
        if user.access_token_expire_date < datetime.now():
            return jsonify({"response": 401})
        
        g.user = user

        return  f(*args, **kwargs)

    return decorated_function


def target_user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        target_username = request.json.get("target_username")
        if not target_username:
            return jsonify({"response": 401})
        
        target_user = UserMain().get_user_query_by_username(target_username)
        g.target_user = target_user

        return f(*args, **kwargs)

    return decorated_function