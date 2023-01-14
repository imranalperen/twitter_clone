from app.db import session
from app.models import Tweets, TweetsLikes, Retweets, Users
from sqlalchemy.sql import and_
from sqlalchemy import desc


class TweetMain:
    def add_tweet(self, user_id, tweet_body, tweet_image, related_tweet_id):
        if not tweet_image:
            if(len(tweet_body) > 280 or len(tweet_body) < 1):
                return {"status": False, "error": 2001}
        
        tweet = Tweets(
            user_id = user_id,
            body = tweet_body,
            image = tweet_image,
            related_tweets = related_tweet_id
        )
        session.add(tweet)
        session.commit()
        return {"status": True}

    def tweet_like(self, user_id, tweet_id):
        query = TweetsLikes(
            tweet_id = tweet_id,
            like_user_id = user_id
        )
        session.add(query)
        session.commit()
        return {"status": True}

    def unlike_tweet(self, user_id, tweet_id):
        (
            session.query(TweetsLikes)
            .where(and_(
                TweetsLikes.tweet_id == tweet_id,
                TweetsLikes.like_user_id == user_id
            ))
            .delete()
        )
        session.commit()
        return {"status": True}

    def retweet_tweet(self, user_id, tweet_id):
        query = Retweets(
            tweet_id = tweet_id,
            rt_user_id = user_id
        )
        session.add(query)
        session.commit()
        return {"status": True}

    def unretweet_tweet(self, user_id, tweet_id):
        (
            session.query(Retweets)
            .where(and_(
                Retweets.rt_user_id == user_id,
                Retweets.tweet_id == tweet_id
            ))
            .delete()
        )
        session.commit()
        return {"status": True}