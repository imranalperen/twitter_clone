import hashlib
import uuid
from datetime import timedelta, date, datetime
import random
from localsettings import MAILJET_API_KEY, MAILJET_SECRET_KEY, ABLY_API_KEY
from mailjet_rest import Client
from ably import AblyRest
from math import pi

def password_hasher(string, salt):
    text = str(string) + str(salt)
    hashed_text = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return hashed_text


def create_access_token():
    token = uuid.uuid4().hex
    create_date = date.today()
    end_date = create_date + timedelta(days=7)
    token_properties = {
        "token": token,
        "end_date": end_date
    }
    return token_properties


def hashtag_finder(tweet_body):
    tag_vocabs = []
    vocabs = tweet_body.split()
    for vocab in vocabs:
        if vocab[0] == "#":
            tag_vocabs.append(vocab)
    return tag_vocabs

def create_verification_code():
    return random.randint(1000, 9999)


def send_verfictaion_code_mail(mail_adress, verification_code):
    api_key = MAILJET_API_KEY
    api_secret = MAILJET_SECRET_KEY
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "toddoregister@protonmail.com",
                    "Name": "Clone Twitter"
                },
                "To": [
                    {
                        "Email": f"{mail_adress}"
                    }
                ],
                "Subject": "Reset Password",
                "TextPart": "",
                "HTMLPart": f"Your verification code for twitter clone reset password: {verification_code}",
                "CustomId": "AppGettingStartedTest"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    if result.status_code == 200:
        return True
    return False


async def publish_message(main_user, chat_id, message_body):
    ably = AblyRest(f'{ABLY_API_KEY}')
    channel = ably.channels.get(f'{chat_id}')
    date_now = str(datetime.now())
    publish_message = {
        "message": message_body,
        "date": date_now,
        "sender_id": main_user.id,
        "chat_id": chat_id
    }
    await channel.publish(f'{chat_id}', publish_message)

async def send_notification_endpoint(user_query, target_user_id, tweet_query, event):
    #if we use target_user_id as channel name then message and notificiations channels will can be same
    #we doesnt want it
    #so we need to salt it easiest way.
    #we can make channel name an irregular number. message channel only have natural numbers
    #so we can multiply with pi
    channel_id = target_user_id * pi
    ably = AblyRest(f'{ABLY_API_KEY}')
    channel = ably.channels.get(f'{channel_id}')
    date_now = str(datetime.now())
    notification = {
        "user_id": user_query.id,
        "name": user_query.name,
        "username": user_query.username,
        "profile_image": user_query.profile_image,
        "tweet_id": tweet_query.id,
        "tweet_body": tweet_query.body,
        "tweet_image": tweet_query.image,
        "date": date_now,
        "event": event
    }
    await channel.publish(f'{target_user_id}', notification)