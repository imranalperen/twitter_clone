import hashlib
import uuid
from datetime import timedelta, date
import random
from localsettings import MAILJET_API_KEY, MAILJET_SECRET_KEY
from mailjet_rest import Client

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