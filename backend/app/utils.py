import hashlib
import uuid
from datetime import timedelta, date


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