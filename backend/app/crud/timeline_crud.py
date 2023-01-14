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
                reply_count = 0
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
                    "reply_count": reply_count,
                    "is_retweeted": False,
                    "is_liked": False
                })
        
        return {"status": True, "tweet": tweet}


class TweetPage:
    def create_tweet_page(self, user, tweet_id):
        #first we control is this a child tweet or is it a mother tweet
        #if it is mother tweet we look for childs
        #if its a child tweet we look for mother
        #so if we check tweet_id s replied_to
        #if replied_to is none then it is a mother tweet but if there is value it is mother tweet
        q = (
            session.query(Tweets)
            .where(Tweets.id == tweet_id)
            .first()
        )
        if q.replied_to:
            #this is a child tweet
            parent_tweet = (
                session.query(Tweets)
                .where(Tweets.id == q.replied_to)
                .first()
            )
            parent_user = (
                session.query(Users)
                .where(Users.id == parent_tweet.user_id)
                .first()
            )
            parent_tweet_list = []

            like_count = (
                session.query(TweetsLikes)
                .where(TweetsLikes.tweet_id == parent_tweet.id)
                .count()
            )
            retweet_count = (
                session.query(Retweets)
                .where(Retweets.tweet_id == parent_tweet.id)
                .count()
            )
            reply_count = (
                session.query(Tweets)
                .where(Tweets.replied_to == parent_tweet.id)
                .count()
            )
            liked_q = (
                session.query(TweetsLikes)
                .where(TweetsLikes.like_user_id == parent_user.id)
                .where(TweetsLikes.tweet_id == parent_tweet.id)
                .first()
            )
            is_liked = False
            if liked_q:
                is_liked = True
            retweeted_q = (
                session.query(Retweets)
                .where(Retweets.rt_user_id == parent_user.id)
                .where(Retweets.tweet_id == parent_tweet.id)
                .first()
            )
            is_retweeted = False
            if retweeted_q:
                is_retweeted = True
            parent_tweet_list.append({
                "tweet_id": parent_tweet.id,
                "user_id": parent_user.id,
                "name": parent_user.name,
                "username": parent_user.username,
                "profile_image": parent_user.profile_image,
                "time_created": parent_tweet.time_created,
                "body": parent_tweet.body,
                "image": parent_tweet.image,
                "like_count": like_count,
                "retweet_count": retweet_count,
                "reply_count": reply_count,
                "is_retweeted": is_retweeted,
                "is_liked": is_liked
            })
            #if there tweets.replied_to is == tweet_id therei s child tweets
            child_tweets_q = (
                session.query(Tweets)
                .where(Tweets.replied_to == tweet_id)
                .all()
            )
            child_tweets = []
            if child_tweets_q:
                for tweet in child_tweets_q:
                    child_tweet_user = (
                        session.query(Users)
                        .where(Users.id == tweet.user_id)
                        .first()
                    )
                    like_count = (
                        session.query(TweetsLikes)
                        .where(TweetsLikes.tweet_id == tweet.id)
                        .count()
                    )
                    retweet_count = (
                        session.query(Retweets)
                        .where(Retweets.tweet_id == tweet_id)
                        .count()
                    )
                    reply_count = (
                        session.query(Tweets)
                        .where(Tweets.replied_to == tweet_id)
                        .count()
                    )
                    liked_q = (
                        session.query(TweetsLikes)
                        .where(TweetsLikes.like_user_id == user.id)
                        .where(TweetsLikes.tweet_id == tweet_id)
                        .first()
                    )
                    is_liked = False
                    if liked_q:
                        is_liked = True
                    retweeted_q = (
                        session.query(Retweets)
                        .where(Retweets.rt_user_id == user.id)
                        .where(Retweets.tweet_id == tweet_id)
                        .first()
                    )
                    is_retweeted = False
                    if retweeted_q:
                        is_retweeted = True
                    child_tweets.append({
                        "tweet_id": tweet.id,
                        "user_id": child_tweet_user.id,
                        "name": child_tweet_user.name,
                        "username": child_tweet_user.username,
                        "profile_image": child_tweet_user.profile_image,
                        "time_created": tweet.time_created,
                        "body": tweet.body,
                        "image": tweet.image,
                        "like_count": like_count,
                        "retweet_count": retweet_count,
                        "reply_count": reply_count,
                        "is_retweeted": is_retweeted,
                        "is_liked": is_liked
                    })
            return {"parent_tweet": parent_tweet_list, "child_tweets": child_tweets}
            

        else:
            #this is a parent tweet
            print("this is a parent tweet")
            



        # #the tweet answered
        # q = (
        #     session.query(Tweets)
        #     .where(Tweets.id == tweet_id)
        # )
        # for t in q:
        #     mother_tweet_id = t.replied_to
        # if not mother_tweet_id:
        #     # mother_tweet = tweet_id
        #     #tweetin kendisini dondurucez
        #     return {"response": 2002}

        # q = (
        #     session.query(Tweets)
        #     .where(Tweets.id == mother_tweet_id)
        # )
        # for i in q:
        #     mother_user_id = i.id
        # #we can reach answered tweets writer and tweet themself so we can crate it now
        # #we will cll this answered tweet as mother_tweet
        # tweet_query = (
        #     session.query(Tweets)
        #     .where(Tweets.id == mother_tweet_id)
        # )
        # user_query = (
        #     session.query(Users)
        #     .where(Users.id == mother_user_id)
        # )
        # mother_tweet_like_count = (
        #     session.query(TweetsLikes)
        #     .where(TweetsLikes.tweet_id == mother_tweet_id)
        #     .count()
        # )
        # mother_tweet_retweet_count = (
        #     session.query(Retweets)
        #     .where(Retweets.tweet_id == mother_user_id)
        #     .count()
        # )
        # is_retweeted_query = (
        #     session.query(Retweets)
        #     .where(Retweets.rt_user_id == user.id)
        #     .where(Retweets.tweet_id == mother_tweet_id)
        # )
        # for i in is_retweeted_query:
        #     is_retweeted = False
        #     if i.id:
        #         is_retweeted = True
        # is_liked_query = (
        #     session.query(TweetsLikes)
        #     .where(TweetsLikes.like_user_id == user.id)
        #     .where(TweetsLikes.tweet_id == mother_tweet_id)
        # )
        # for i in is_liked_query:
        #     is_liked = False
        #     if i.id:
        #         is_liked = True

        # mother_tweet = []
        # for t in tweet_query:
        #     for u in user_query:
        #         mother_tweet.append({
        #             "tweet_id": t.id,
        #             "user_id": u.id,
        #             "name": u.name,
        #             "username": u.username,
        #             "profile_image": u.profile_image,
        #             "time_created": t.time_created,
        #             "body": t.body,
        #             "image": t.image,
        #             "like_count": mother_tweet_like_count,
        #             "retweet_count": mother_tweet_retweet_count,
        #             "is_retweeted": is_retweeted,
        #             "is_liked": is_liked
        #         })
        # print(mother_tweet)
        # return {"mother_tweet": mother_tweet}
        # #now we can get all replies it wont be same like twitter it ll be more basic

