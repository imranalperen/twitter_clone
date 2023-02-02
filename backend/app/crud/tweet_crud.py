from app.db import session
from app.models import Tweets, TweetsLikes, Retweets, Tags
from app.crud.timeline_crud import TimelineMain
from sqlalchemy.sql import and_, desc
from app.utils import hashtag_finder
from config import UPLOAD_FOLDER_URL


class TweetMain:
    def add_tweet(self, user_id, tweet_body, tweet_image, replied_to_id):
        if not tweet_image:
            if(len(tweet_body) > 280 or len(tweet_body) < 1):
                return {"status": False, "error": 2001}
        
        if tweet_image:
            tweet_image = UPLOAD_FOLDER_URL + tweet_image
            
        tweet = Tweets(
            user_id = user_id,
            body = tweet_body,
            image = tweet_image,
            replied_to = replied_to_id
        )
        session.add(tweet)
        session.commit()
        #if tweet has any hashtag we will add these tagas hashtags table
        tag_vocabs = hashtag_finder(tweet_body)
        if tag_vocabs:
        #we already add the tweet we need last tweet of user
            last_tweet = TimelineMain().last_tweet(user_id)
            tweet_id = last_tweet["tweet"][0]["tweet_id"]
            for vocab in tag_vocabs:
                q = Tags(
                    tweet_id = tweet_id,
                    user_id = user_id,
                    tag_vocab = vocab
                )
                session.add(q)
                session.commit()
                
        return {"status": True}

    def tweet_like(self, user_id, tweet_id):
        query = TweetsLikes(
            tweet_id = tweet_id,
            like_user_id = user_id
        )
        session.add(query)
        session.commit()

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

    def retweet_tweet(self, user_id, tweet_id):
        query = Retweets(
            tweet_id = tweet_id,
            rt_user_id = user_id
        )
        session.add(query)
        session.commit()


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
        
    def delete_tweet_endpoint(self, tweet_id):
        (
            session.query(Tweets)
            .where(Tweets.id == f"{tweet_id}")
            .update({
                "is_deleted": True,
            })
        )
        session.commit()