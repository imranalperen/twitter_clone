from app.db import session
from app.models import Users, UsersFollowers, Tweets, TweetsLikes, Retweets
from sqlalchemy.sql import and_, desc
from sqlalchemy import func

class WhoToFollow:
    def recommend_two_user(self, main_user_id):       
        query = (
            session.query(Users)
            .outerjoin(UsersFollowers, and_(
                UsersFollowers.following_user_id==Users.id,
                UsersFollowers.main_user_id==main_user_id
                )
            )
            .where(UsersFollowers.id==None)
            .where(Users.id!=main_user_id)
            .order_by(func.random())
            .limit(2)
            .all()
        )
        # from sqlalchemy.dialects import postgresql
        # x = str(q.statement.compile(dialect=postgresql.dialect()))
        recommended_users = []
        for user in query:
            recommended_users.append({
                "id": user.id,
                "name": user.name,
                "username": user.username,
                "is_following": False,
                "image": user.profile_image
            })

        return recommended_users

class TimelineMain:
    def create_timeline(self, user):
        #tweets of following users
        q1 = (
            session.query(
                Users.id,
                Users.name,
                Users.username,
                Users.profile_image,
                Tweets.time_created,
                Tweets.body,
                Tweets.id.label("tweet_id"),
                Tweets.image,
                Tweets.replied_to
            )
            .join(Tweets, Tweets.user_id == Users.id)
            .join(UsersFollowers, UsersFollowers.following_user_id == Users.id)
            .where(UsersFollowers.main_user_id == user.id)        
            )
        #tweets of main user
        q2 = (
            session.query(
                Users.id,
                Users.name,
                Users.username,
                Users.profile_image,
                Tweets.time_created,
                Tweets.body,
                Tweets.id.label("tweet_id"),
                Tweets.image,
                Tweets.replied_to
            )
            .join(Tweets, Tweets.user_id == Users.id)
            .join(UsersFollowers, UsersFollowers.main_user_id == Users.id)
            .where(UsersFollowers.main_user_id == user.id)    
        )
        #mergeing 2 queries and sort results descending tweet create time
        q = q1.union(q2).order_by(Tweets.time_created.desc()).all()
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

            reply_count = (
                session.query(Tweets)
                .where(Tweets.replied_to == tweet.tweet_id)
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
                "reply_count": reply_count,
                "replied_to": tweet.replied_to,
            })
        return {"status": True, "tweets": tweets}

    
    def user_liked_tweets(self, user_id):
        q = (
        session.query(TweetsLikes)
        .where(TweetsLikes.like_user_id == user_id)
        )
        liked_tweets = []
        for like in q:
            liked_tweets.append({
                "tweet_id": like.tweet_id,
            })

        return {"status": True, "liked_tweets": liked_tweets}


    def user_retweeted_tweets(self, user_id):
        q = (
            session.query(Retweets)
            .where(Retweets.rt_user_id == user_id)
        )
        retweeted_tweets = []
        for retweet in q:
            retweeted_tweets.append({
                "tweet_id": retweet.tweet_id
            })

        return {"status": True, "retweeted_tweets": retweeted_tweets}

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


class TweetPage:
    def create_tweet_page(self, user, tweet_id):
        #the tweet answered
        q = (
            session.query(Tweets)
            .where(Tweets.id == tweet_id)
        )

        for t in q:
            answered_tweet_id = t.replied_to
        if not answered_tweet_id:
            return {"response": 1}
        
        answered_tweet_query = (
            session.query(Tweets)
            .where(Tweets.id == answered_tweet_id)
        )
        answered_tweet = []
        for i in answered_tweet_query:
            answered_tweet.append({
                "tweet_id": i.tweet_id,

            })

