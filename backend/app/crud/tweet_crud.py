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

    
    def get_answer_tweets(self, main_tweet_id):
        q = (
            session.query(
                Users.id,
                Users.name,
                Users.username,
                Users.profile_image,
                Tweets.time_created,
                Tweets.body,
                Tweets.id.label("tweet_id"),
                Tweets.image,
                Tweets.related_tweets
            )
            .join(Tweets, Tweets.user_id == Users.id)
            .where(Tweets.related_tweets == main_tweet_id)
            
        )
        
        if not q:
            return {"status": False, "error": 2002}

        tweets = []
        for tweet in q:
            like_count = (
                session.query(TweetsLikes)
                .where(TweetsLikes.tweet_id == tweet.tweet_id)
                .count()
            )

            retweet_count = (
                session.query(Retweets)
                .where(Retweets.tweet_id == tweet.tweet_id)
                .count()
            )

            tweets.append({
                "tweet_id": tweet.tweet_id,
                "user_id": tweet.id,
                "name": tweet.name,
                "username": tweet.username,
                "profile_image": tweet.profile_image,
                "time_created": tweet.time_created,
                "body": tweet.body,
                "image": tweet.image,
                "like_count": like_count,
                "retweet_count": retweet_count,
            })

        return {"status": True, "tweets": tweets}
