answerler twets tablosuna eklendigi icin refresh atilinca anasayfaya dusuyor fakat releted tweet olarak dusmesi lazim ayar ver
zincirleme answerler serisi varsa ilk twite git oradan gostermeye basla
like lenen retweeetlenen tweetler anasayfaya dusmuyor ayar ver
tweet silmeyi tweetlerin dbsini hallettikten sonra yap

tweets tablosuna answer_to ekle fk ile bagla

tweet page de artilacak requestte 
tiklanan twite bagli olan ve bagli oldugu twitleri alman ve donmen lazim

trend topic icin
eger atilan tweette #lorem varsa # ler icin ayri bir tablo olustur ve atilan twitteki # kelimesini o tabloya ekle, tabloda son n saatte en cok girilen # kelimelerini yakala ve onalri trend topic olarak kokle


mesajlasma
mesajlasma baslarken kime inputu olacak inputa kelime @.... isim girildikce kisiler onerecek takip ettikleri oncelikli olacak sekilde
mesajaslma basladiginda mesaj okuma ve yollama 2 func olucak okuma computed de olucak surekli olarak db yi kontrol edecek yeni mesaj varmi id farkli mesaj buldummu ekrana basacak gonderen zaten db ye mesaj eklicen ez

bildiirmler
bildirimler icinde computed kullanilabilir denenmesi lazim kafada ta mbisi sekillenmedi
bunlar yapilsa yeter reis baya bi is olur sonunda


hic kimseyi takip etmiyorken twit atinca anasyfa sapiyior fixle






createtimeline:
userin kendi tweetlerinin query si
takip ettiklerinin query si
birlestirme
tweetler = []
toplam_query loop
    like_count func
    retweet_count func
    reply_count func
    is_liked_query func
    is_retweeted_query func
    tweetler.append = [{
        tweet_id,
        user_id,
        name,
        username,
        profile_image,
        time_created,
        body,
        image,
        like_count,
        retweet_count,
        reply_count,
        replied_to,
        is_retweeted,
        is_liked
    }]


last_tweet:
tweet_query
user_query
tweet= []
like_count = 0
retweet_count = 0
reply_count = 0
query loop
    tweet_id,
    user_id,
    name,
    username,
    profile_image,
    time_created,
    body,
    image,
    like_count,
    retweet_count,
    reply_count,
    replied_to
    is_retweeted,
    is_liked,


create_tweet_page:
child_tweets=[]
parent_tweet=[]
for parent tweet:
    parent_tweet_query
    parent_tweet_user_query
    parent_tweet_like_count,
    parent_tweet_retweet_count,
    parent_tweet_reply_count,
    parent_tweet_is_liked_query,
    parent_tweet_is_retweeted_query,
    parent_tweet.appen 
        tweet_id
        user_id
        name
        username
        profile_image
        time_created
        body
        image
        like_count
        retweet_count
        reply_count
        replied_to
        is_retweeted
        is_liked

child_tweets_query
for child tweets:
    tweet_user_query
    like_count
    retweet_count
    reply_count
    is_liked
    is_retweeted
    child_tweets.appen
        tweet_id
        user_id
        name
        username
        profile_image
        time_created
        body
        image
        like_count
        retweet_count
        reply_count
        replied_to
        is_retweeted
        is_liked



yapi 4 yerde kullaniliyor.
en belirgin fark child twetlerde replied to yok gerisi tamamen ayni