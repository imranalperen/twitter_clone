from app.db import session
from app.models import Tweets, TweetsLikes, Retweets,Users
from sqlalchemy.sql import and_
from sqlalchemy import desc


class TweetMain:
    def add_tweet(self, user, tweet_body, tweet_image):
        if not tweet_image:
            if(len(tweet_body) > 280 or len(tweet_body) < 1):
                return {"status": False, "error": 2001}
        
        tweet = Tweets(
            user_id = user.id,
            body = tweet_body,
            image = tweet_image
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

    def last_tweet(self, user_id):
        tweet_query = (
            session.query(Tweets)
            .where(Tweets.user_id == user_id)
            .order_by(desc(Tweets.id))
            .limit(1)
        )
        user_query = (
            session.query(Users)
            .where(Users.id == user_id)
        )
        tweet = []
        for t in tweet_query:
            for u in user_query:
                like_count = 0
                retweet_count = 0
                tweet.append({
                    "tweet_id": t.id,
                    "user_id": u.id,
                    "name": u.name,
                    "username": u.username,
                    "profile_image": u.profile_image,
                    "time_created": t.time_created,
                    "body": t.body,
                    "image": t.image,
                    "like_count": like_count,
                    "retweet_count": retweet_count,
                    "is_retweeted": False,
                    "is_liked": False
                })
        
        return {"status": True, "tweet": tweet}
        
        


