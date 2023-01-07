from app.db import session
from app.models import Tweets


class TweetMain:
    def add_tweet(self, user, tweet_body, tweet_image):
        if(len(tweet_body) > 280 or len(tweet_body) < 1):
            return {"status": False, "error": 2001}
        
        tweet = Tweets(user_id = user.id, body = tweet_body, image = tweet_image)
        session.add(tweet)
        session.commit()
        return {"status": True}