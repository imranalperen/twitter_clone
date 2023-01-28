from app.db import session
from app.models import Users, UsersFollowers, Tweets, TweetsLikes, Retweets, Tags
from sqlalchemy.sql import and_, desc
from sqlalchemy import func

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

    
    def create_topic_page(self, topic, user):
        q = (
            session.query(
                Tags,
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
            .join(Tweets, Tweets.id == Tags.tweet_id)
            .join(Users, Users.id == Tweets.user_id)
            .where(Tags.tag_vocab == f"#{topic}")
            .order_by(Tweets.time_created.desc())
            .limit(100)
            .all()
        )

        tweets = []
        for tweet in q:
            tweet_interactions = TimelineUtils.get_tweet_interactions(self, 
                tweet_id = tweet.tweet_id,
                user_id = user.id,
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


class WhoToFollow:
    def who_to_follow_feed(self, user_id):
        query = (
            session.query(Users)
            .outerjoin(UsersFollowers, and_(
                UsersFollowers.following_user_id == Users.id,
                UsersFollowers.main_user_id == user_id
                )
            )
            .where(UsersFollowers.id == None)
            .where(Users.id != user_id)
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
        #retweets of main user
        # SELECT * FROM users
        # INNER JOIN  tweets ON tweets.user_id = users.id
        # INNER JOIN users_followers ON users_followers.following_user_id = users.id
        # INNER JOIN retweets ON retweets.tweet_id = tweets.id
        # WHERE (retweets.rt_user_id = 6)
        # q3 = (
        #     session.query(
        #         Users.id,
        #         Users.name,
        #         Users.username,
        #         Users.profile_image,
        #         Tweets.time_created,
        #         Tweets.body,
        #         Tweets.id.label("tweet_id"),
        #         Tweets.image,
        #         Tweets.replied_to
        #     )
        #     .join(Tweets, Tweets.user_id == Users.id)
        #     .join(UsersFollowers, UsersFollowers.following_user_id == Users.id)
        #     .join(Retweets, Retweets.tweet_id == Tweets.id)
        #     .where(Retweets.rt_user_id == user.id)
        # )
        #we need retweets of following users and likes of following users

        #mergeing 2 queries and sort results descending tweet create time
        q = q1.union(q2).order_by(Tweets.time_created.desc()).all()
        if not q:
            return {"status": False, "error": 2002}

        tweets = []
        for tweet in q:
            tweet_interactions = TimelineUtils.get_tweet_interactions(self, 
                tweet_id = tweet.tweet_id,
                user_id = user.id,
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
    def create_tweet_page(self, user_id, tweet_id):
        '''2 situations
        1. this is a parent tweet. list the child tweets of parent tweet
        2. this is a replied tweet. find the parent tweet and list the other child tweets'''
        #first learn is it parent or not
        parent_tweet_query = (
            session.query(Tweets)
            .where(Tweets.id == tweet_id)
            .first()
        )

        parent_tweet = []
        replied_tweet = []
        child_tweets = []
        if not parent_tweet_query.replied_to:
            #this is a parent tweet
            #so we can return argument tweet_id tweet as parent
            #after we can reach childs and return
            #? parent tweet
            parent_tweet_user = (
                session.query(Users)
                .join(Tweets, Tweets.user_id == Users.id)
                .where(Tweets.id == tweet_id)
                .first()
            )
            tweet_interactions = TimelineUtils.get_tweet_interactions(self, 
                tweet_id = tweet_id,
                user_id = user_id,
            )
            parent_tweet.append({
                "tweet_id": parent_tweet_query.id,
                "user_id": parent_tweet_user.id,
                "name": parent_tweet_user.name,
                "username": parent_tweet_user.username,
                "profile_image": parent_tweet_user.profile_image,
                "time_created": parent_tweet_query.time_created,
                "body": parent_tweet_query.body,
                "image": parent_tweet_query.image,
                "like_count": tweet_interactions["like_count"],
                "retweet_count": tweet_interactions["retweet_count"],
                "reply_count": tweet_interactions["reply_count"],
                "replied_to": parent_tweet_query.replied_to,
                "is_retweeted": tweet_interactions["is_retweeted"],
                "is_liked": tweet_interactions["is_liked"]
            })
            #now we have parent tweet we can find and return child twets
            #?child tweets
            child_tweets_query = (
                session.query(Tweets)
                .join(Users, Users.id == Tweets.user_id)
                .where(Tweets.replied_to == tweet_id)
                .all()
            )

        else:
            #this is a child tweet
            #first we find parent tweet and we will return this parent
            #then return tweet id as replied tweet
            #then return child tweets of replied tweet
            #?parent tweet
            parent_tweet_id = parent_tweet_query.replied_to

            parent_tweet_query = (
                session.query(Tweets)
                .join(Users, Users.id == Tweets.user_id)
                .where(Tweets.id == parent_tweet_id)
                .first()
            )
            parent_tweet_user = (
                session.query(Users)
                .where(Users.id == parent_tweet_query.user_id)
                .first()
            )
            tweet_interactions = TimelineUtils.get_tweet_interactions(self, 
                tweet_id = parent_tweet_query.id,
                user_id = user_id,
            )
            parent_tweet.append({
                "tweet_id": parent_tweet_query.id,
                "user_id": parent_tweet_user.id,
                "name": parent_tweet_user.name,
                "username": parent_tweet_user.username,
                "profile_image": parent_tweet_user.profile_image,
                "time_created": parent_tweet_query.time_created,
                "body": parent_tweet_query.body,
                "image": parent_tweet_query.image,
                "like_count": tweet_interactions["like_count"],
                "retweet_count": tweet_interactions["retweet_count"],
                "reply_count": tweet_interactions["reply_count"],
                "replied_to": parent_tweet_query.replied_to,
                "is_retweeted": tweet_interactions["is_retweeted"],
                "is_liked": tweet_interactions["is_liked"]
            })
            #? replied tweet
            replied_tweet_query = (
                session.query(Tweets)
                .join(Users, Users.id == Tweets.user_id)
                .where(Tweets.id == tweet_id)
                .first()
            )
            replied_tweet_user = (
                session.query(Users)
                .where(Users.id == replied_tweet_query.user_id)
                .first()
            )
            tweet_interactions = TimelineUtils.get_tweet_interactions(self,
                tweet_id = replied_tweet_query.id,
                user_id = replied_tweet_user.id
            )

            replied_tweet.append({
                "tweet_id": replied_tweet_query.id,
                "user_id": replied_tweet_user.id,
                "name": replied_tweet_user.name,
                "username": replied_tweet_user.username,
                "profile_image": replied_tweet_user.profile_image,
                "time_created": replied_tweet_query.time_created,
                "body": replied_tweet_query.body,
                "image": replied_tweet_query.image,
                "like_count": tweet_interactions["like_count"],
                "retweet_count": tweet_interactions["retweet_count"],
                "reply_count": tweet_interactions["reply_count"],
                "replied_to": replied_tweet_query.replied_to,
                "is_retweeted": tweet_interactions["is_retweeted"],
                "is_liked": tweet_interactions["is_liked"]
            })
            #? child tweets
            child_tweets_query = (
                session.query(Tweets)
                .join(Users, Users.id == Tweets.user_id)
                .where(Tweets.replied_to == replied_tweet_query.id)
                .all()
            )

        
        for tweet in child_tweets_query:
            user = (
                session.query(Users)
                .join(Tweets, Tweets.user_id == Users.id)
                .where(Tweets.id == tweet.id)
                .first()
            )
            tweet_interactions = TimelineUtils.get_tweet_interactions(self,
                tweet_id = tweet.id,
                user_id = user_id,
            )
            child_tweets.append({
                "tweet_id": tweet.id,
                "user_id": user.id,
                "name": user.name,
                "username": user.username,
                "profile_image": user.profile_image,
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
        
        return {"parent_tweet": parent_tweet, "replied_tweet": replied_tweet, "child_tweets": child_tweets}
    
    
class Explore:
    def create_explore_timeline(self, user_id):
        '''random 50 tweets will be explore feed'''        
        tweets_query = (
            session.query(
                Users.id,
                Users.name,
                Users.username,
                Users.profile_image,
                Tweets.time_created,
                Tweets.body,
                Tweets.id.label("tweet_id"),
                Tweets.image,
                Tweets.replied_to,
                Tweets.user_id
            )
            .join(Tweets, Tweets.user_id == Users.id)
            .order_by(func.random())
            .limit(50)
            .all()
        )

        tweets = []
        for t in tweets_query:
            user_query = (
                session.query(Users)
                .where(Users.id == t.user_id)
            )
            for u in user_query:
                tweet_interactions = TimelineUtils.get_tweet_interactions(self, 
                    tweet_id = t.id,
                    user_id = user_id,
                )
                tweets.append({
                    "tweet_id": t.tweet_id,
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

        return {"status": True, "tweets": tweets}

class UserProfileFeed:
    def get_user_profile_infos(self, username, user):
        q = (
            session.query(Users)
            .where(Users.username == username)
            .first()
        )
        follow_count = (
            session.query(UsersFollowers)
            .where(UsersFollowers.main_user_id == q.id)
            .count()
        )
        followers_count = (
            session.query(UsersFollowers)
            .where(UsersFollowers.following_user_id == q.id)
            .count()
        )
        if user.username == username:
            follwing_sitation = "edit_profile"
        else:
            follwing_sitation = (
                session.query(UsersFollowers)
                .where(and_(
                    UsersFollowers.main_user_id == user.id,
                    UsersFollowers.following_user_id == q.id
                ))
                .first()
            )
            if follwing_sitation:
                follwing_sitation = "unfollow"
            else:
                follwing_sitation = "follow"

        user_info = []
        user_info.append({
            "username": q.username,
            "name": q.name,
            "profile_image": q.profile_image,
            "user_id": q.id,
            "follow_count": follow_count,
            "followers_count": followers_count,
            "following_situation": follwing_sitation,
            "biography": q.biography
        })
        return user_info
    
    def get_user_tweets(self, username, user_id, profile_tab):        
        if profile_tab == "tweets":
            tweets_query = (
                session.query(
                    Users.id,
                    Users.name,
                    Users.username,
                    Users.profile_image,
                    Tweets.time_created,
                    Tweets.body,
                    Tweets.id.label("tweet_id"),
                    Tweets.image,
                    Tweets.replied_to,
                    Tweets.user_id
                )
                .join(Tweets, Tweets.user_id == Users.id)
                .where(Users.username == username)
                .order_by(Tweets.time_created.desc())
                .all()
            )
        if profile_tab == "media":
            tweets_query = (
                session.query(
                    Users.id,
                    Users.name,
                    Users.username,
                    Users.profile_image,
                    Tweets.time_created,
                    Tweets.body,
                    Tweets.id.label("tweet_id"),
                    Tweets.image,
                    Tweets.replied_to,
                    Tweets.user_id
                )
                .join(Tweets, Tweets.user_id == Users.id)
                .where(and_(
                    Users.username == username,
                    Tweets.image != None
                ))
                .order_by(Tweets.time_created.desc())
                .all()
            )
        if profile_tab == "likes":
            #current viewing profile user query
            q = (
                session.query(Users)
                .where(Users.username == username)
                .first()
            )
            tweets_query = (
                session.query(
                    Users.id,
                    Users.name,
                    Users.username,
                    Users.profile_image,
                    Tweets.time_created,
                    Tweets.body,
                    Tweets.id.label("tweet_id"),
                    Tweets.image,
                    Tweets.replied_to,
                    Tweets.user_id
                )
                # .join(Tweets, Tweets.user_id == Users.id)
                # .join(TweetsLikes, TweetsLikes.like_user_id == Tweets.id)
                .join(Tweets, Tweets.user_id == Users.id)
                .join(TweetsLikes, TweetsLikes.tweet_id == Tweets.id)
                .where(TweetsLikes.like_user_id == q.id)
                .order_by(TweetsLikes.like_date.desc())
                .all()
            )
        tweets = []

        for t in tweets_query:
            tweet_interaction = TimelineUtils.get_tweet_interactions(
                self,
                tweet_id = t.tweet_id,
                user_id = user_id
            )

            tweets.append({
                "tweet_id": t.tweet_id,
                "user_id": t.id,
                "name": t.name,
                "username": t.username,
                "profile_image": t.profile_image,
                "time_created": t.time_created,
                "body": t.body,
                "image": t.image,
                "like_count": tweet_interaction["like_count"],
                "retweet_count": tweet_interaction["retweet_count"],
                "reply_count": tweet_interaction["reply_count"],
                "replied_to": t.replied_to,
                "is_retweeted": tweet_interaction["is_retweeted"],
                "is_liked": tweet_interaction["is_liked"],
            })
        return {"status": True, "tweets": tweets}