from app.db import session
from app.models import Users, UsersFollowers, Tweets, TweetsLikes, Retweets, Tags
from sqlalchemy.sql import and_, desc
from sqlalchemy import func
from collections import Counter

class TrendTopics:
    def get_trends(self):
        #we pick trends in last 100 tweets
        #most 5 hashtag in last 100 tweets will be trends
        q = (
            session.query(Tags.tag_vocab)
            .order_by(Tags.id.desc())
            .limit(100)
            .all()
        )

        count = {}
        
        for i in q:           
            if not i[0] in count:
                count[i[0]] = 1
            else:
                count[i[0]] += 1

        sorted_counts = sorted(count.items(), key=lambda x: x[1])
        #key of trends dict is tag name and value is count of tweets
        trends = sorted_counts[-1: -6: -1]
        return trends


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

class TimelineUtils:
    def get_tweet_interactions(self, **kwargs):
        like_count = (
            session.query(TweetsLikes)
            .where(TweetsLikes.tweet_id == kwargs["tweet_id"])
            .count()
        )
        retweet_count = (
            session.query(Retweets)
            .where(Retweets.tweet_id == kwargs["tweet_id"])
            .count()
        )
        reply_count = (
            session.query(Tweets)
            .where(Tweets.replied_to == kwargs["tweet_id"])
            .count()
        )
        is_liked_query = (
            session.query(TweetsLikes)
            .where(TweetsLikes.tweet_id == kwargs["tweet_id"])
            .where(TweetsLikes.like_user_id == kwargs["user_id"])
            .first()
        )
        try:
            if is_liked_query.id:
                is_liked = True
        except:
            is_liked = False
        
        is_retweeted_query = (
            session.query(Retweets)
            .where(Retweets.tweet_id == kwargs["tweet_id"])
            .where(Retweets.rt_user_id == kwargs["user_id"])
            .first()
        )
        try:
            if is_retweeted_query.id:
                is_retweeted = True
        except:
            is_retweeted = False

        tweet_interactions = {
            "like_count": like_count,
            "retweet_count": retweet_count,
            "reply_count": reply_count,
            "is_liked": is_liked,
            "is_retweeted": is_retweeted
        }
        return tweet_interactions

            

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
            tweet_interactions = TimelineUtils.get_tweet_interactions(self, 
                tweet_id = tweet.tweet_id,
                user_id = tweet.id,
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
                "like_count": tweet_interactions["like_count"],
                "retweet_count": tweet_interactions["retweet_count"],
                "reply_count": tweet_interactions["reply_count"],
                "replied_to": tweet.replied_to,
                "is_retweeted": tweet_interactions["is_retweeted"],
                "is_liked": tweet_interactions["is_liked"]
            })
        return {"status": True, "tweets": tweets}


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
                tweet_interactions = TimelineUtils.get_tweet_interactions(self, 
                    tweet_id = t.id,
                    user_id = u.id,
                )
                tweet.append({
                    "tweet_id": t.id,
                    "user_id": u.id,
                    "name": u.name,
                    "username": u.username,
                    "profile_image": u.profile_image,
                    "time_created": t.time_created,
                    "body": t.body,
                    "image": t.image,
                    "like_count": tweet_interactions["like_count"],
                    "retweet_count": tweet_interactions["retweet_count"],
                    "reply_count": tweet_interactions["reply_count"],
                    "replied_to": t.replied_to,
                    "is_retweeted": tweet_interactions["is_retweeted"],
                    "is_liked": tweet_interactions['is_liked']
                })
        
        return {"status": True, "tweet": tweet}


class TweetPage:
    def create_tweet_page(self, user, tweet_id):
        """we need parent tweet which replied
        and we need all the child tweets of this parent
        first we check is tweet parent or not
        if tweet is parent then we just look for child tweets
        if twet is child tweet we find the parent tweet
        and we get the all child tweets"""
        clicked_tweet = (
            session.query(Tweets)
            .where(Tweets.id == tweet_id)
            .first()
        )
        child_tweets = []
        parent_tweet = []
        is_it_parent = False

        if not clicked_tweet.replied_to:
            #this is a parent tweet
            parent_tweet_query = (
                session.query(Tweets)
                .where(Tweets.id == clicked_tweet.id)
                .first()
            )
            is_it_parent = True                
        else:
            #this is a child tweet
            #replies of replied tweet so
            #first we get parent of child then child
            parent_tweet_query = (
                session.query(Tweets)
                .where(Tweets.id == clicked_tweet.replied_to)
                .first()
            )

        parent_tweet_user_query = (
                session.query(Users)
                .where(Users.id == parent_tweet_query.user_id)
                .first()
            )
        tweet_interactions = TimelineUtils.get_tweet_interactions(self, 
                tweet_id = parent_tweet_query.id,
                user_id = user.id,
            )
        parent_tweet.append({
                "tweet_id": parent_tweet_query.id,
                "user_id": parent_tweet_user_query.id,
                "name": parent_tweet_user_query.name,
                "username": parent_tweet_user_query.username,
                "profile_image": parent_tweet_user_query.profile_image,
                "time_created": parent_tweet_query.time_created,
                "body": parent_tweet_query.body,
                "image": parent_tweet_query.image,
                "like_count": tweet_interactions["like_count"],
                "retweet_count": tweet_interactions["retweet_count"],
                "reply_count": tweet_interactions["reply_count"],
                "is_retweeted": tweet_interactions["is_retweeted"],
                "replied_to": parent_tweet_query.replied_to,
                "is_liked": tweet_interactions["is_liked"]
            })
        #if it is not parent tweet we need to get replied_to mean parent of child twet
        if not is_it_parent:
            child_tweets_query = (
                session.query(Tweets)
                .where(Tweets.replied_to == clicked_tweet.replied_to)
                .all()
            )
        else:
            child_tweets_query = (
                session.query(Tweets)
                .where(Tweets.replied_to == clicked_tweet.id)
                .all()
            )
            
        for t in child_tweets_query:
            tweet_user = (
                session.query(Users)
                .where(Users.id == t.user_id)
                .first()
            )

            tweet_interactions = TimelineUtils.get_tweet_interactions(self, 
                tweet_id = t.id,
                user_id = tweet_user.id,
            )
                
            child_tweets.append({
                "tweet_id": t.id,
                "user_id":tweet_user.id,
                "name": tweet_user.name,
                "username": tweet_user.username,
                "profile_image": tweet_user.profile_image,
                "time_created": t.time_created,
                "body": t.body,
                "image": t.image,
                "like_count": tweet_interactions["like_count"],
                "retweet_count": tweet_interactions["retweet_count"],
                "reply_count": tweet_interactions["reply_count"],
                "is_retweeted": tweet_interactions["is_retweeted"],
                "is_liked": tweet_interactions["is_liked"]
            })


        
        return {"status": True, "parent_tweet": parent_tweet, "child_tweets": child_tweets}
