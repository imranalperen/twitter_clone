<template>
<div class="home_container">
    <main_tweet
        :user="user"
        @refresh_tweets="add_new_tweet()"
    />
    <div class="timeline" v-if="timeline_elements != 2002">
        <div v-for="tweet in timeline_elements" class="timeline_tweet_container">
            <div class="tweet_top_bar" v-if="tweet.replied_to">
                <img src="@/assets/icons8-speech-bubble-50.png" class="comment_image_small">
                <p>{{ tweet.username }} replied</p>
            </div>
            <div class="tweet_container_main">
                <div class="left">
                    <div class="tweet_profile_image">
                        <a href="">
                            <img :src="tweet.profile_image">
                        </a>
                    </div>
                </div>
                <div class="right">
                    <div class="right_top_bar">
                        <div class="user_info">
                        <a href="">
                            <div class="name"><p>{{ tweet.name }}</p></div>
                        </a>
                        <div class="username"><p>@{{ tweet.username }}</p></div>
                        <div class="tweet_time"><p>{{ tweet.time_created }}</p></div>
                        </div>
                        <div class="delete_tweet_container" v-if="tweet.user_id == user.id">
                            <img src="@/assets/icons8-trash-bin-32.png">
                        </div>
                    </div>
                    <div class="tweet_body" @click="redirect_tweet_page(tweet.tweet_id)">
                        <div class="tweet_text" v-if="tweet.body">
                            {{ tweet.body }}
                        </div>
                        <div class="tweet_image" v-if="tweet.image">
                            <img :src="tweet.image">
                        </div>
                    </div>
                    <div class="interaction_footer">
                        <div class="comment_container">
                            <img src="@/assets/icons8-speech-bubble-50.png" class="comment_image" @click="toggle_reply_container(tweet.tweet_id)">
                            <p class="comment_count">{{ tweet.reply_count }}</p>
                        </div>
                        <div class="retweet_container" v-if="tweet.is_retweeted" @click="unretweet(tweet.tweet_id)">
                            <img src="@/assets/icons8-retweet-24.png" class="unretweet_image">
                            <p class="retweet_count">{{ tweet.retweet_count }}</p>
                        </div>
                        <div class="retweet_container" v-else @click="retweet(tweet.tweet_id)">
                            <img src="@/assets/icons8-retweet-24.png" class="retweet_image">
                            <p class="retweet_count">{{ tweet.retweet_count }}</p>
                        </div>

                        <div class="like_container" v-if="tweet.is_liked" @click="unlike_tweet(tweet.tweet_id)">
                            <img src="@/assets/icons8-heart-50.png" class="unlike_image">
                            <p class="like_count">{{ tweet.like_count }}</p>
                        </div>
                        <div class="like_container" v-else @click="like_tweet(tweet.tweet_id)">
                            <img src="@/assets/icons8-heart-50.png" class="like_image">
                            <p class="like_count">{{ tweet.like_count }}</p>
                        </div>
                    </div>
                    <div class="reply_component" v-if="tweet.tweet_id == toggle_reply_id">
                        <reply_tweet
                            :toggle_reply_id = "toggle_reply_id"
                        ></reply_tweet>
                    </div>
                </div>
            </div>
        </div>
    </div>


    <div class="timeline" v-else>
        user follows noone recommend users for user 
    </div>
</div>
</template>

<script>
import main_tweet from '@/components/main/main_tweet.vue'
import reply_tweet from '@/components/main/reply_tweet.vue'

import {
    timeline_request,
    like_request,
    main_user_liked_tweets,
    unlike_request,
    retweet_request,
    unretweet_request,
    main_user_retweeted_tweets,
    last_tweet_of_user_request,
} from '@/requests'


export default {
    components: {
        main_tweet,
        reply_tweet
    },

    props: ["user"],

    data() {
        return {
            timeline_elements: [],
            toggle_reply_id: null,
        }
    },

    async beforeCreate() {
        let response_value = await timeline_request()
        this.timeline_elements = response_value.response

        //icon color change for liked tweets
        let liked_tweets_object = await main_user_liked_tweets()
        //includes() function cant use to numbers we need to convert string
        let liked_tweets_string = []
        for(let i = 0; i < liked_tweets_object.response.length; i++) {
            liked_tweets_string.push(liked_tweets_object.response[i].tweet_id)
        }
        //we r adding is_liked to timeline element
        for(let i = 0; i < this.timeline_elements.length; i++) {
            this.timeline_elements[i].is_liked = false
            if(liked_tweets_string.includes(this.timeline_elements[i].tweet_id)) {
                this.timeline_elements[i].is_liked = true
            }
        }

        //icon color change for retweeted tweets
        let retweeted_tweets_object = await main_user_retweeted_tweets()
        let retweeted_tweets_string = []
        for(let i = 0; i < retweeted_tweets_object.response.length; i++) {
            retweeted_tweets_string.push(retweeted_tweets_object.response[i].tweet_id)
        }
        for(let i = 0; i < this.timeline_elements.length; i++) {
            this.timeline_elements[i].is_retweeted = false
            if(retweeted_tweets_string.includes(this.timeline_elements[i].tweet_id)) {
                this.timeline_elements[i].is_retweeted = true
            }
        }

    },

    methods: {

        toggle_reply_container(tweet_id) {
            if(this.toggle_reply_id) {
                this.toggle_reply_id = null
            }
            else {
                this.toggle_reply_id = tweet_id
            }
        },

        async add_new_tweet() {
            let new_tweet_object = await last_tweet_of_user_request()
            this.timeline_elements = [new_tweet_object.response[0]].concat(this.timeline_elements)
        },

        async like_tweet(tweet_id) {
            let request_body = {
                "tweet_id": tweet_id
            }
            let response_value = await like_request(request_body)
            if(response_value.response) {
                for(let i = 0; i < this.timeline_elements.length; i++) {
                    if(this.timeline_elements[i].tweet_id == tweet_id) {
                        this.timeline_elements[i].is_liked = true
                        this.timeline_elements[i].like_count += 1
                    }
                }
            }
        },

        async unlike_tweet(tweet_id) {
            let request_body = {
                "tweet_id": tweet_id
            }
            let response_value = await unlike_request(request_body)
            
            if(response_value) {
                for(let i = 0; i < this.timeline_elements.length; i++) {
                    if(this.timeline_elements[i].tweet_id == tweet_id) {
                        this.timeline_elements[i].is_liked = false
                        this.timeline_elements[i].like_count -= 1
                    }
                }
            }
        },

        async retweet(tweet_id) {
            let request_body = {
                "tweet_id": tweet_id
            }
            let response_value = await retweet_request(request_body)
            if(response_value.response) {
                for(let i = 0; i < this.timeline_elements.length; i++) {
                    if(this.timeline_elements[i].tweet_id == tweet_id) {
                        this.timeline_elements[i].is_retweeted = true
                        this.timeline_elements[i].retweet_count += 1
                    }
                }
            }
        },

        async unretweet(tweet_id) {
            let request_body = {
                "tweet_id": tweet_id
            }
            let response_value = await unretweet_request(request_body)
            if(response_value.response) {
                for(let i = 0; i < this.timeline_elements.length; i++) {
                    if(this.timeline_elements[i].tweet_id == tweet_id) {
                        this.timeline_elements[i].is_retweeted = false
                        this.timeline_elements[i].retweet_count -= 1
                    }
                }
            }
        },

        redirect_tweet_page(tweet_id) {
            this.$router.push({ name: 'tweet_page', params: { id: `${tweet_id}` } })
        }

    },
}

</script>

<style scoped>
.timeline_tweet_container {
    border-bottom: 1px solid var(--bordergray);
    padding: .3em 1em;
}

.tweet_top_bar {
    display: flex;
}

.tweet_top_bar > p {
    font-size: .8em;
    font-weight: bold;
    color: var(--bordergray);
    margin-left: .3em;
}


.tweet_container_main {
    display: flex;
}

.right {
    display: flex;
    flex-direction: column;
    margin-top: .3em;
    width: 100%;
}

.right_top_bar {
    display: flex;
    justify-content: space-between;
}

.user_info {
    display: flex;
}

.tweet_body {
    display: flex;
    flex-direction: column;
    cursor: pointer;
}

.interaction_footer {
    display: flex;
    justify-content: space-around;
}

.tweet_profile_image > a > img {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin-right: .7em;
    margin-top: .5em;
}

.name > p {
    margin-right: .4em;
    font-weight: bold;
}

.username > a > p {
    color: var(--bordergray);
}

.tweet_time > p {
    margin-left: .4em;
    color: var(--bordergray);
}

a {
    text-decoration: none;
}

.tweet_text {
    margin: .3em 0;
}

.tweet_image {
    margin-bottom: .3em;
}
.tweet_image > img {
    max-width:  530px;
    max-height: 530px;
    border-radius: 25px;
}

.comment_container, .like_container, .retweet_container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: .3em;
    cursor: pointer;
}

.comment_image, .retweet_image, .like_image, .unlike_image, .unretweet_image {
    width: 24px;
    height: 24px;
    filter: invert(32%) sepia(6%) saturate(811%) hue-rotate(166deg) brightness(97%) contrast(89%);
}

.comment_image_small {
    width: 18px;
    height: 18px;
    filter: invert(32%) sepia(6%) saturate(811%) hue-rotate(166deg) brightness(97%) contrast(89%);
}

.unlike_image {
    filter: invert(30%) sepia(76%) saturate(1852%) hue-rotate(310deg) brightness(94%) contrast(90%);
}

.unretweet_image {
    filter: invert(61%) sepia(47%) saturate(424%) hue-rotate(95deg) brightness(97%) contrast(89%);
}
.comment_container:hover, .like_container:hover, .retweet_container:hover {
    padding: .3em;
    border-radius: 35px;
}
.comment_container:hover {
    /* var(--tweetBtnBg) renk kodu */
    filter: invert(44%) sepia(45%) saturate(1867%) hue-rotate(180deg) brightness(103%) contrast(88%);
}

.like_container:hover {
    /* var(--like);  renk kodu*/
    filter: invert(30%) sepia(76%) saturate(1852%) hue-rotate(310deg) brightness(94%) contrast(90%);
}

.retweet_container:hover {
    /* var(--retweet);  color code*/
    filter: invert(61%) sepia(47%) saturate(424%) hue-rotate(95deg) brightness(97%) contrast(89%);
}

.comment_count, .retweet_count, .like_count {
    margin-left: .3em;
    font-size: .8em;
    color: var(--bordergray);
}
.delete_tweet_container > img {
    width: 20px;
    filter: invert(35%) sepia(84%) saturate(2760%) hue-rotate(314deg) brightness(93%) contrast(93%);
    cursor: pointer;
}

.delete_tweet_container:hover {
    filter: invert(12%) sepia(88%) saturate(3896%) hue-rotate(348deg) brightness(127%) contrast(106%);
}
</style>