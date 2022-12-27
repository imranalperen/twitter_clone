from flask import(
    Blueprint,
    request,
    jsonify
)
from app.crud.users_crud import UserRegistration
from app.utils import create_access_token


main = Blueprint("main", __name__, url_prefix="/api")

@main.route("signup", methods=["POST"])
def signup():
    name = request.json.get("name")
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    register_response = UserRegistration().signup(name, username, email, password)
    #{"status": Bool, "message": "string"}
    
    if register_response["status"]:
        return jsonify({"response": True})
    
    return jsonify({"response": register_response["message"]})

@main.route("login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    login_response = UserRegistration().login(username, password)
    if login_response["status"]:
        access_token = create_access_token()
        UserRegistration().update_acces_token(username, access_token)
        return jsonify({"response": True, "access_token": access_token})

    return jsonify({"response": login_response["message"]})