from flask import(
    Blueprint,
    request,
    jsonify,
    g
)
from app.crud.users_crud import UserFollow, UserRegistration, UserMain
from app.crud.tweet_crud import TweetMain
from app.utils import create_access_token
from app.decorators import login_required


main = Blueprint("main", __name__, url_prefix="/api")


@main.route("signup", methods=["POST"])
def signup():
    name = request.json.get("name")
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    register_response = UserRegistration().signup(name, username, email, password)
    #{"status": Bool, "error": error code}
    
    if register_response["status"]:
        return jsonify({"response": True})
    
    return jsonify({"response": register_response["error"]})


@main.route("login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    login_response = UserRegistration().login(username, password)
    if login_response["status"]:
        access_token = create_access_token()
        UserRegistration().update_acces_token(username, access_token)
        return jsonify({"response": True, "access_token": access_token})

    return jsonify({"response": login_response["error"]})


@main.route("registration_info", methods=["POST"])
@login_required
def registration_info():
    user = g.user
    image = request.json.get("profile_image")
    date_of_birth = request.json.get("date_of_birth")
    gender = request.json.get("gender")
    UserRegistration().update_user_info(user, image, date_of_birth, gender)
    return jsonify({"response": True})



@main.route("user", methods=["POST"])
@login_required
def user():
    user = g.user
    return jsonify({
        "username": user.username,
        "name": user.name,
        "image": user.profile_image
    })


@main.route("recommend_follow_user", methods=["GET"])
@login_required
def recommend_follow_user():
    main_user = g.user
    recommended_users = UserFollow().recommend_two_user(main_user.id)
    return jsonify({"response": recommended_users})


@main.route("follow_user", methods=["GET"])
@login_required
def follow_user():
    main_user = g.user
    following_user_id = request.headers.get("user-id")
    UserFollow().follow_user(main_user, following_user_id)
    return jsonify({"response": True})


@main.route("unfollow_user", methods=["GET"])
@login_required
def unfollow_user():
    main_user = g.user
    unfollowing_user_id = request.headers.get("user-id")
    UserFollow().unfollow_user(main_user, unfollowing_user_id)
    return jsonify({"response": True})


@main.route("post_tweet", methods=["POST"])
@login_required
def tweet():
    user = g.user
    tweet_body = request.headers.get("tweet-body")
    tweet_response = TweetMain().add_tweet(user, tweet_body)
    if tweet_response["status"]:
        return jsonify({"response": True})
    
    return jsonify({"response": tweet_response["error"]})


@main.route("timeline", methods=["GET"])
@login_required
def timeline():
    #imranalperen fakueser1
    user = g.user
    tweets = UserMain().create_timeline(user)
    if not tweets["status"]:
        return jsonify({"response": tweets["error"]})
    
    return jsonify({"response": tweets["tweets"]})