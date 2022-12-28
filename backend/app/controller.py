from flask import(
    Blueprint,
    request,
    jsonify,
    g
)
from app.crud.users_crud import UserMain
from app.utils import create_access_token
from app.decorators import login_required


main = Blueprint("main", __name__, url_prefix="/api")


@main.route("signup", methods=["POST"])
def signup():
    name = request.json.get("name")
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    register_response = UserMain().signup(name, username, email, password)
    #{"status": Bool, "message": error code}
    
    if register_response["status"]:
        return jsonify({"response": True})
    
    return jsonify({"response": register_response["message"]})


@main.route("login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    login_response = UserMain().login(username, password)
    if login_response["status"]:
        access_token = create_access_token()
        UserMain().update_acces_token(username, access_token)
        return jsonify({"response": True, "access_token": access_token})

    return jsonify({"response": login_response["message"]})


@main.route("timeline", methods=["POST"])
@login_required
def home():
    #TODO timelineyi dolduracak tweetleri alip response olarak onlari don
    access_token = request.headers.get("access-token")
    user = g.user
    return jsonify({
        "username": user.username,
        "name": user.name
    })