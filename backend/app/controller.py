from flask import(
    Blueprint,
    request,
    jsonify,
    g
)
from app.crud.users_crud import UserMain, TweetMain
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
def timeline():
    #TODO timelineyi dolduracak tweetleri alip response olarak onlari don
    user = g.user
    return jsonify({
        "username": user.username,
        "name": user.name
    })


@main.route("post_tweet", methods=["POST"])
@login_required
def tweet():
    user = g.user
    tweet_body = request.headers.get("tweet-body")
    tweet_response = TweetMain().add_tweet(user, tweet_body)
    if tweet_response["status"]:
        return jsonify({"response": True})
    
    return jsonify({"response": tweet_response["message"]})


@main.route("recommend_follow_user", methods=["GET"])
@login_required
def recommend_follow_user():
    main_user = g.user
    main_user_follow_list = UserMain().get_user_follow_list_by_id(main_user.id)
    print(main_user_follow_list)
    recommended_users = UserMain().recommend_two_user(main_user_follow_list, main_user.id)

    return jsonify({"response": recommended_users})


@main.route("follow_user", methods=["GET"])
@login_required
def follow_user():
    main_user = g.user
    following_user_id = request.headers.get("user-id")
    UserMain().follow_user(main_user, following_user_id)
    return jsonify({"response": True})


@main.route("unfollow_user", methods=["GET"])
@login_required
def unfollow_user():
    main_user = g.user
    unfollowing_user_id = request.headers.get("user-id")
    UserMain().unfollow_user(main_user, unfollowing_user_id)
    return jsonify({"response": True})