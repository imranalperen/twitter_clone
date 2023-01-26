from flask import(
    Blueprint,
    request,
    jsonify,
    g
)
from app.crud.users_crud import UserFollow, UserRegistration
from app.crud.tweet_crud import TweetMain
from app.crud.fake_crud import FakeMain
from app.crud.timeline_crud import TimelineMain, WhoToFollow, TweetPage, TrendTopics, Explore, UserProfileFeed
from app.utils import create_access_token
from app.decorators import login_required


main = Blueprint("main", __name__, url_prefix="/api")

@main.route("create_fake_users", methods=["POST", "GET"])
def create_fake_user():
    fake_user_response = (
        FakeMain().create_fake_users(),
        FakeMain().follow_fake_users(),
        FakeMain().create_fake_tweets()
    )
    
    return jsonify({"response": fake_user_response})

@main.route("signup", methods=["POST"])
def signup():
    name = request.json.get("name")
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    register_response = UserRegistration().signup(name, username, email, password)    
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
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "profile_image": user.profile_image
    })


@main.route("recommend_follow_user", methods=["GET"])
@login_required
def recommend_follow_user():
    main_user = g.user
    recommended_users = WhoToFollow().recommend_two_user(main_user.id)
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
    tweet_body = request.json.get("tweet_body")
    tweet_image = request.json.get("tweet_image")
    replied_to_id = None
    tweet_response = TweetMain().add_tweet(user.id, tweet_body, tweet_image, replied_to_id)
    if tweet_response["status"]:
        return jsonify({"response": True})
    
    return jsonify({"response": tweet_response["error"]})


@main.route("timeline", methods=["GET"])
@login_required
def timeline():
    user = g.user
    tweets = TimelineMain().create_timeline(user)
    if not tweets["status"]:
        return jsonify({"response": tweets["error"]})
    
    return jsonify({"response": tweets["tweets"]})


@main.route("like_tweet", methods=["POST"])
@login_required
def like_tweet():
    user_id = g.user.id
    tweet_id = request.json.get("tweet_id")
    TweetMain().tweet_like(user_id, tweet_id)
    return jsonify({"response": True})


@main.route("unlike_tweet", methods=["POST"])
@login_required
def unlike_tweet():
    user_id = g.user.id
    tweet_id = request.json.get("tweet_id")
    TweetMain().unlike_tweet(user_id, tweet_id)
    return jsonify({"resposne": True})


@main.route("retweet", methods=["POST"])
@login_required
def retweet():
    user_id = g.user.id
    tweet_id = request.json.get("tweet_id")
    TweetMain().retweet_tweet(user_id, tweet_id)
    return jsonify({"response": True})


@main.route("unretweet", methods=["POST"])
@login_required
def unretweet():
    user_id = g.user.id
    tweet_id = request.json.get("tweet_id")
    TweetMain().unretweet_tweet(user_id, tweet_id)
    return jsonify({"response": True})


@main.route("user_last_tweet", methods=["GET"])
@login_required
def user_last_tweet():
    user = g.user.id
    last_tweet = TimelineMain().last_tweet(user)
    return jsonify({"response": last_tweet["tweet"]})
    

@main.route("add_replied_tweet", methods=["POST"])
@login_required
def add_replied_tweet():
    user = g.user
    tweet_body = request.json.get("tweet_body")
    tweet_image = request.json.get("tweet_image")
    replied_to_id = request.json.get("tweet_id")
    tweet_response = TweetMain().add_tweet(user.id, tweet_body, tweet_image, replied_to_id)
    if tweet_response["status"]:
        return jsonify({"response": True})
    
    return jsonify({"response": tweet_response["error"]})


@main.route("tweet_page", methods=["POST"])
@login_required
def tweet_page():
    user = g.user
    tweet_id = request.json.get("tweet_id")
    tweet_page_response = TweetPage().create_tweet_page(user, tweet_id)
    return jsonify({"response": tweet_page_response})


@main.route("trend_topics", methods=["POST"])
@login_required
def trend_topics():
    trends = TrendTopics().get_trends()
    return jsonify({"response": trends})


@main.route("trend/<string:topic>")
@login_required
def trend_page(topic):
    user = g.user
    tweets = TrendTopics().create_topic_page(topic, user)
    return jsonify({"response": tweets["tweets"]})


@main.route("explore", methods=["POST"])
@login_required
def explore_page():
    user = g.user
    tweets = Explore().create_explore_timeline(user.id)
    return jsonify({"response": tweets["tweets"]})


@main.route("profile", methods=["POST"])
@login_required
def user_profile():
    username = request.json.get("username")
    user = g.user
    user_profile = UserProfileFeed().get_user_profile_infos(username, user)
    return jsonify({"response": user_profile})


@main.route("profile_tweets", methods=["POST"])
@login_required
def profile_tweets():
    username = request.json.get("username")
    user_id = g.user.id
    purpose = "tweets"
    user_tweets = UserProfileFeed().get_user_tweets(username, user_id, purpose)
    return jsonify({"response": user_tweets["tweets"]})


@main.route("profile_feed", methods=["POST"])
@login_required
def profile_feed():
    username = request.json.get("username")
    user_id = g.user.id
    profile_tab = request.json.get("profile_tab")
    tweets = UserProfileFeed().get_user_tweets(username, user_id, profile_tab)
    return jsonify({"response": tweets["tweets"]})