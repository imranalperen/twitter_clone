from app.db import session
from app.models import Users, UsersFollowers, Tweets, TweetsLikes
from app.utils import password_hasher

class FakeMain():
    def create_fake_users(self):
        password = "qweasd"
        username = "user1"
        hashed_password = password_hasher(password, username)
        user1 = Users(
            name = "user1",
            username = "user1",
            email = "user1",
            hashed_password = hashed_password
        )
        session.add(user1)
        session.commit()
        password = "qweasd"
        username = "user2"
        user2 = Users(
            name = "user2",
            username = "user2",
            email = "user2",
            hashed_password = hashed_password
        )
        session.add(user2)
        session.commit()
        password = "qweasd"
        username = "user3"
        user3 = Users(
            name = "user3",
            username = "user3",
            email = "user3",
            hashed_password = hashed_password
        )
        session.add(user3)
        session.commit()
        password = "qweasd"
        username = "user4"
        user4 = Users(
            name = "user4",
            username = "user4",
            email = "user4",
            hashed_password = hashed_password
        )
        session.add(user4)
        session.commit()
        password = "qweasd"
        username = "user5"
        user5 = Users(
            name = "user5",
            username = "user5",
            email = "user5",
            hashed_password = hashed_password
        )
        session.add(user5)
        session.commit()

    def follow_fake_users(self):
        query = UsersFollowers(
            main_user_id = 1,
            following_user_id = 2
        )
        session.add(query)
        session.commit()

        query = UsersFollowers(
            main_user_id = 1,
            following_user_id = 4
        )
        session.add(query)
        session.commit()

        query = UsersFollowers(
            main_user_id = 2,
            following_user_id = 5
        )
        session.add(query)
        session.commit()

        query = UsersFollowers(
            main_user_id = 2,
            following_user_id = 4
        )
        session.add(query)
        session.commit()

        query = UsersFollowers(
            main_user_id = 2,
            following_user_id = 3
        )
        session.add(query)
        session.commit()

        query = UsersFollowers(
            main_user_id = 2,
            following_user_id = 1
        )
        session.add(query)
        session.commit()

        query = UsersFollowers(
            main_user_id = 3,
            following_user_id = 4
        )
        session.add(query)
        session.commit()

        query = UsersFollowers(
            main_user_id = 3,
            following_user_id = 1
        )
        session.add(query)
        session.commit()

        query = UsersFollowers(
            main_user_id = 4,
            following_user_id = 2
        )
        session.add(query)
        session.commit()

        query = UsersFollowers(
            main_user_id = 4,
            following_user_id = 5
        )
        session.add(query)
        session.commit()

        query = UsersFollowers(
            main_user_id = 5,
            following_user_id = 3
        )
        session.add(query)
        session.commit()

        query = UsersFollowers(
            main_user_id = 5,
            following_user_id = 1
        )
        session.add(query)
        session.commit()

    def create_fake_tweets(self):
        tweet = Tweets(user_id = 1, body = "user1 den tweet atmaca")
        session.add(tweet)
        session.commit()
        tweet = Tweets(user_id = 1, body = "user1 den sondan bir once")
        session.add(tweet)
        session.commit()
        tweet = Tweets(user_id = 2, body = "user2 benim ulan")
        session.add(tweet)
        session.commit()
        tweet = Tweets(user_id = 5, body = "user5 salak sacma twitler")
        session.add(tweet)
        session.commit()
        tweet = Tweets(user_id = 2, body = "user2 sjw erlik")
        session.add(tweet)
        session.commit()
        tweet = Tweets(user_id = 1, body = "user1 den kolpa twit cekelim biraz")
        session.add(tweet)
        session.commit()
        tweet = Tweets(user_id = 3, body = "user3 sut icen bayir domuzu")
        session.add(tweet)
        session.commit()
        tweet = Tweets(user_id = 3, body = "user3 user 3 den 2 twit yeter panpa")
        session.add(tweet)
        session.commit()
        tweet = Tweets(user_id = 4, body = "user4 abi cok iyi yaa")
        session.add(tweet)
        session.commit()
        tweet = Tweets(user_id = 1, body = "user1 den alksdj")
        session.add(tweet)
        session.commit()
        tweet = Tweets(user_id = 4, body = "user4 bu enerji sako mu")
        session.add(tweet)
        session.commit()
        tweet = Tweets(user_id = 2, body = "user2 den merhaba")
        session.add(tweet)
        session.commit()
        tweet = Tweets(user_id = 1, body = "user1 den zor olacak buralrai doldurmak")
        session.add(tweet)
        session.commit()
        tweet = Tweets(user_id = 4, body = "user4 beler cok mu zor")
        session.add(tweet)
        session.commit()       
        tweet = Tweets(user_id = 5, body = "user5 bu skiller halis mi")
        session.add(tweet)
        session.commit()
