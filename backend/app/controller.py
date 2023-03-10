from flask import(
    Blueprint,
    request,
    jsonify,
    g
)
from app.crud.users_crud import UserFollow, UserRegistration, UserMain
from app.crud.tweet_crud import TweetMain
from app.crud.timeline_crud import (
    TimelineMain,
    WhoToFollow,
    TweetPage,
    TrendTopics,
    Explore,
    UserProfileFeed
)
from app.crud.messages_crud import MessagesMain
from app.utils import create_access_token
from app.decorators import login_required, target_user_required
from app.utils import create_verification_code, send_verfictaion_code_mail, publish_message
import uuid
import os
import asyncio


main = Blueprint("main", __name__, url_prefix="/api")


#! REGISTRATION
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


@main.route("send_verify_code", methods=["POST"])
def send_verify_code():
    mail_adress = request.json.get("mail_adress")
    user = UserRegistration().get_user_by_mail(mail_adress)
    if user:
        verification_code = create_verification_code()
        if send_verfictaion_code_mail(mail_adress, verification_code):
            UserRegistration().save_verfication_code(user, verification_code)
            return {"response": True}
        #if not return valid response probably there is no more free
        return {"response": 9001}

    return {"response": 1002}

@main.route("reset_password", methods=["POST"])
def reset_password():
    verify_code = request.json.get("verify_code")
    password = request.json.get("password")
    email = request.json.get("email")
    user = UserRegistration().get_user_by_mail(email)
    if UserRegistration().compare_verification_codes(user, verify_code):
        UserRegistration().update_user_password(user, password)
        return {"response": True}
    return {"response": 1004}
    


@main.route("registration_info", methods=["POST"])
@login_required
def registration_info():
    user = g.user
    bio = request.form.get("bio")
    file_name = str(uuid.uuid4()) + '.png'
    file = request.files.get("file")
    if not file:
        file_name = "anonim_image.jpeg"
    else:
        #DEVELOPMENT
        from . import app
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    UserRegistration().update_user_profile_image(user, file_name, bio)
    return jsonify({"response": True})

#!GENERAL
@main.route("user", methods=["POST"])
@login_required
def user():
    user = g.user
    user_information = UserMain().get_user_by_username(user.username)
    return jsonify({"response": user_information})


@main.route("recommend_follow_user", methods=["GET"])
@login_required
def recommend_follow_user():
    user = g.user
    recommended_users = WhoToFollow().who_to_follow_feed(user.id)
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


@main.route("timeline", methods=["GET"])
@login_required
def timeline():
    user = g.user
    tweets = TimelineMain().create_timeline(user)    
    return jsonify({"response": tweets["tweets"]})

#!TWEET INTERACTIONS
@main.route("like_tweet", methods=["POST"])
@login_required
def like_tweet():
    user_id = g.user.id
    tweet_id = request.json.get("tweet_id")
    TweetMain().tweet_like(user_id, tweet_id)
    event = 'like'
    TweetMain().send_notification(user_id, tweet_id, event)
    return jsonify({"response": True})


@main.route("unlike_tweet", methods=["POST"])
@login_required
def unlike_tweet():
    user_id = g.user.id
    tweet_id = request.json.get("tweet_id")
    TweetMain().unlike_tweet(user_id, tweet_id)
    event = 'like'
    TweetMain().delete_notification(user_id, tweet_id, event)
    return jsonify({"resposne": True})


@main.route("retweet", methods=["POST"])
@login_required
def retweet():
    user_id = g.user.id
    tweet_id = request.json.get("tweet_id")
    TweetMain().retweet_tweet(user_id, tweet_id)
    event = 'retweet'
    TweetMain().send_notification(user_id, tweet_id, event)
    return jsonify({"response": True})


@main.route("unretweet", methods=["POST"])
@login_required
def unretweet():
    user_id = g.user.id
    tweet_id = request.json.get("tweet_id")
    TweetMain().unretweet_tweet(user_id, tweet_id)
    event = 'retweet'
    TweetMain().delete_notification(user_id, tweet_id, event)
    return jsonify({"response": True})


@main.route("user_last_tweet", methods=["GET"])
@login_required
def user_last_tweet():
    user = g.user.id
    last_tweet = TimelineMain().last_tweet(user)
    return jsonify({"response": last_tweet["tweet"]})


#! TWEET CRUD
@main.route("post_tweet", methods=["POST"])
@login_required
def tweet():
    user = g.user
    tweet_body = request.form.get("tweet_body")
    file = request.files.get("file")
    file_name = None
    replied_to_id = None
    if file:
        #DEVELOPMENT
        from . import app
        file_name = str(uuid.uuid4()) + '.png'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    tweet_response = TweetMain().add_tweet(user.id, tweet_body, file_name, replied_to_id)
    if tweet_response["status"]:
        return jsonify({"response": True})
    
    return jsonify({"response": tweet_response["error"]})


@main.route("delete_tweet", methods=["POST"])
@login_required
def delete_tweet():
    tweet_id = request.json.get("tweet_id")
    TweetMain().delete_tweet_endpoint(tweet_id)
    return({"response": True})

@main.route("add_replied_tweet", methods=["POST"])
@login_required
def add_replied_tweet():
    user = g.user
    tweet_body = request.form.get("tweet_body")
    file = request.files.get("file")
    file_name = None
    if file:
        #DEVELOPMENT
        from . import app
        file_name = str(uuid.uuid4()) + '.png'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    replied_to_id = request.form.get("reply_id")
    tweet_response = TweetMain().add_tweet(user.id, tweet_body, file_name, replied_to_id)
    if tweet_response["status"]:
        event = 'reply'
        TweetMain().send_notification(user.id, replied_to_id, event)
        return jsonify({"response": True})
    
    return jsonify({"response": tweet_response["error"]})

#!TWEET PAGE
@main.route("tweet_page", methods=["POST"])
@login_required
def tweet_page():
    user = g.user
    tweet_id = request.json.get("tweet_id")
    tweet_page_response = TweetPage().create_tweet_page(user.id, tweet_id)
    return jsonify({"response": tweet_page_response})


@main.route("last_reply_of_user", methods=["POST"])
@login_required
def last_reply():
    user = g.user
    tweet_id = request.json.get("tweet_id")
    tweet_page_response = TweetPage().last_reply_of_tweet(user.id, tweet_id)
    return jsonify({"response": tweet_page_response})


#!TRENDS
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

#!EXPLORE
@main.route("explore", methods=["POST"])
@login_required
def explore_page():
    user = g.user
    tweets = Explore().create_explore_timeline(user.id)
    return jsonify({"response": tweets["tweets"]})

#! PROFILE
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

@main.route("edit_profile", methods=["POST"])
@login_required
def edit_profile():
    user = g.user
    name = request.form.get("name")
    bio = request.form.get("bio")
    file = request.files.get('file')
    file_name = None
    if file:
        from . import app
        file_name = str(uuid.uuid4()) + '.png'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    #DEVELOPMENT
    UserRegistration().edit_user_profile(user, file_name, name ,bio)
    return jsonify({"response": True})

@main.route("follows_and_followers", methods=["POST"])
@login_required
def follows_and_followers():
    user_id = g.user.id
    visit_user_id = request.json.get("visit_user_id")
    purpose = request.json.get("purpose")
    response_body = UserFollow().get_user_follows_or_followers(visit_user_id, purpose, user_id)
    return jsonify({"response": response_body})


#! MESSAGES
@main.route("user_profile_image", methods=["POST"])
@login_required
@target_user_required
def user_profile_image():
    profile_image = g.target_user.profile_image
    # return jsonify({"response": profile_image.profile_image})
    return jsonify({"response": profile_image})


@main.route("chat_history", methods=["POST"])
@login_required
@target_user_required
def chat_history_endpoint():
    main_user = g.user
    target_user = g.target_user
    chat_history = MessagesMain().get_chat_history(main_user, target_user)
    return jsonify({"response": chat_history})

@main.route("get_chat_id", methods=["POST"])
@login_required
@target_user_required
def get_chat_id_endpoint():
    main_user = g.user
    target_user = g.target_user
    chat_id = MessagesMain().get_chat_id(main_user, target_user)
    return jsonify({"response": chat_id})


@main.route("post_message", methods=["POST"])
@login_required
@target_user_required
def post_message_endpoint():
    main_user = g.user
    target_user = g.target_user
    message_body = request.json.get("message_body")
    chat_id = MessagesMain().get_chat_id(main_user, target_user)
    MessagesMain().post_message(main_user, chat_id, message_body)
    asyncio.run(publish_message(main_user, chat_id, message_body))
    return jsonify({"response": "1"})


@main.route("chat_contacts", methods=["POST"])
@login_required
def chat_contacts_endpoint():
    user = g.user
    chat_contacts = MessagesMain().get_user_chat_contacts(user)
    return jsonify({"response": chat_contacts})


@main.route("mark_as_read", methods=["POST"])
@login_required
def mark_as_read_endpoint():
    user = g.user
    chat_id = request.json.get("chat_id")
    MessagesMain().mark_as_read(user, chat_id)
    return jsonify({"response": 1})

@main.route("mark_as_read_notifications", methods=["POST"])
@login_required
def mark_as_read_notifications_endpoint():
    user = g.user
    UserMain().mark_as_read_notifications(user.id)
    return jsonify({"response": 1})

#! notifications
@main.route("notifications", methods=["POST"])
@login_required
def notifications_endpoint():
    user = g.user
    notifications = UserMain().user_notifications(user.id)
    return jsonify({"response": notifications})

@main.route("notification_counts", methods=["POST"])
@login_required
def notification_count_endpoint():
    user = g.user
    notification_count = UserMain().notifications_count(user.id)
    return jsonify({"response": notification_count})


#! SEARCH ENGINE
@main.route("search_users", methods=["POST"])
@login_required
def search_users_endpoint():
    keyword = request.json.get("keyword")
    search_results = UserMain().search_users(keyword)
    return jsonify({"response": search_results})