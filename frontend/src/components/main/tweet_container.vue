<template>
<div class="tweet_general_container">
    <div class="timeline" v-if="tweets != 2002">
        <div 
            v-for="tweet in tweets"
            :key="tweet.tweet_id"
            class="timeline_tweet_container"
            :class="{big: is_big == true}" @click="route_click(tweet)"
        >
            <div v-if="!tweet.is_deleted">
                <div class="tweet_top_bar" v-if="tweet.replied_to && !is_tweet_page_reply">
                    <img src="@/assets/icons8-speech-bubble-50.png" class="comment_image_small">
                    <p class="replied_username">{{ tweet.username }} replied</p>
                </div>
                <div class="tweet_container_main">
                    <div class="left">
                        <div class="tweet_profile_image_container">
                            <img :src="tweet.profile_image" class="tweet_profile_image" :class="{big_image: is_big == true}">
                        </div>
                        <div v-if="is_parent" class="connect_line">
                        </div>
                    </div>
                    <div class="right">
                        <div class="right_top_bar">
                            <div class="user_info">
                                <div class="name_contaienr"><p class="name">{{ tweet.name }}</p></div>
                                <div class="username_container"><p class="username">@{{ tweet.username }}</p></div>
                                <!-- TODO time created i duzenle  -->
                                <!-- <div class="tweet_time"><p>{{ tweet.time_created }}</p></div> -->
                                <div class="tweet_time"><p>1h</p></div>
                            </div>
                            <div class="delete_tweet_container" v-if="tweet.user_id == user.id" @click="delete_tweet(tweet.tweet_id)">
                                <img src="@/assets/icons8-trash-bin-32.png" class="delete_image">
                            </div>
                        </div>
                        <div class="tweet_body">
                            <div class="tweet_text_container" v-if="tweet.body">
                                <p class="tweet_body_text"><span class="tweet_body_text" v-html="calculate_hashtag(tweet.body)"></span></p>
                            </div>
                            <div class="tweet_image" v-if="tweet.image">
                                <img :src="tweet.image" class="tweet_body_image">
                            </div>
                        </div>
                        <div class="interaction_footer">
                            <div class="comment_container" @click="toggle_reply_container(tweet.tweet_id)">
                                <img src="@/assets/icons8-speech-bubble-50.png" class="comment_image">
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
                                @add_replied_tweet_timeline = add_new_tweet_timeline_emit(tweet.tweet_id)
                            ></reply_tweet>
                        </div>
                    </div>
                </div>
            </div>
            <div class="deleted_tweet" v-if="tweet.is_deleted">
                <deleted_tweet/>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import reply_tweet from '@/components/main/reply_tweet.vue'
import deleted_tweet from '@/components/main/deleted_tweet.vue'

import {
    like_request,
    unlike_request,
    retweet_request,
    unretweet_request,
    delete_tweet_request
} from '@/requests'

export default {
    components: {
        reply_tweet,
        deleted_tweet
    },

    props: ["tweets", "user", "is_big", "is_tweet_page_reply", "is_parent"],

    emits: [
        "add_new_tweet_timeline_emit",
    ],
    
    data() {
        return {
            toggle_reply_id: null,
            tweet_body: null,
            delete_tweet_bool: false
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
        
        add_new_tweet_timeline_emit(tweet_id) {
            this.$emit("add_new_tweet_timeline_emit", tweet_id)
            if(tweet_id) {
                for(let i = 0; i < this.tweets.length; i++) {
                    if(this.tweets[i].tweet_id == tweet_id) {
                        this.tweets[i].reply_count += 1
                        this.toggle_reply_container(tweet_id)
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
                for(let i = 0; i < this.tweets.length; i++) {
                    if(this.tweets[i].tweet_id == tweet_id) {
                        this.tweets[i].is_retweeted = false
                        this.tweets[i].retweet_count -= 1
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
                for(let i = 0; i < this.tweets.length; i++) {
                    if(this.tweets[i].tweet_id == tweet_id) {
                        this.tweets[i].is_retweeted = true
                        this.tweets[i].retweet_count += 1
                    }
                }
            }
        },

        async like_tweet(tweet_id) {
            let request_body = {
                "tweet_id": tweet_id
            }
            let response_value = await like_request(request_body)
            if(response_value.response) {
                for(let i = 0; i < this.tweets.length; i++) {
                    if(this.tweets[i].tweet_id == tweet_id) {
                        this.tweets[i].is_liked = true
                        this.tweets[i].like_count += 1
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
                for(let i = 0; i < this.tweets.length; i++) {
                    if(this.tweets[i].tweet_id == tweet_id) {
                        this.tweets[i].is_liked = false
                        this.tweets[i].like_count -= 1
                    }
                }
            }
        },
        
        calculate_hashtag(tweet) {
            let tweet_body = tweet
            if(tweet.includes("#")) {
                let vocabs = tweet.split(" ")
                for(let i = 0; i < vocabs.length; i++) {
                    if(vocabs[i].includes("#")) {
                        //TODO hashtag in tweet link it topic
                        //vue warn maximum recursive updates exceeded.
                        vocabs[i] = `<a class=hashtag_keyword>${vocabs[i]}</a>`
                        tweet_body = vocabs.join(" ")
                    }
                }
            }
            return tweet_body
        },

        route_click(tweet) {
            let e = event.target.className
            let topic_vocab = event.target.innerHTML
            e = e.split(" ")[0]
            //tweet_profile_image, name, username   redirects profile
            if(e == 'tweet_profile_image' || e == 'name' || e == 'username') {
                this.$router.push({name: 'profile', params:{string: tweet.username, profile_tab :null}})
            }
            //tweet_body_text, interaction_footer, left, timeline_tweet_container redirects tweet_page
            else if (e == 'timeline_tweet_container' || e == 'tweet_body_text' || e == 'left' || e == 'right_top_bar' || e == 'interaction_footer' || e == 'tweet_top_bar' || e == 'replied_username' || e == 'comment_image_small' || e == 'tweet_body_image') {
                this.$router.push({name: 'tweet_page', params:{id: tweet.tweet_id}})
            }
            //hashtag_keyword redirects topic page
            else if (e == 'hashtag_keyword') {
                topic_vocab = topic_vocab.split("#")[1]
                this.$router.push({name: 'topic', params:{string: topic_vocab}})
            }
        },

        async delete_tweet(tweet_id) {
            let response_value = await delete_tweet_request(tweet_id)
        }
    },
}

</script>

<style scoped>

.replied_username {
    cursor: pointer;
}

.comment_image_small {
    cursor: pointer;
}

.left {
    display: flex;
    flex-direction: column;
}
.connect_line {
    height: 100%;
    border-left: 3px solid var(--bordergray);
    margin-left: 30px;  /* set this value related to profile big_image*/
}
.big {
    font-size: 1.2em;
    font-weight: 500;
    border-bottom: none !important;
    padding: 0 1em 0 1em !important;
}

.big_image {
    width: 60px !important;
    height: 60px !important;
}
.timeline_tweet_container {
    border-bottom: 1px solid var(--bordergray);
    padding: .6em .6em .5em .6em;
    cursor: pointer;
}

.tweet_top_bar {
    display: flex;
    margin-bottom: .5em;
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

.tweet_profile_image {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin-right: .7em;
    cursor: pointer;
    /* margin-top: .5em; */
}

.name {
    margin-right: .4em;
    font-weight: bold;
    cursor: pointer;
}

.username {
    color: var(--bordergray);
    cursor: pointer;
}

.tweet_time > p {
    margin-left: .4em;
    color: var(--bordergray);
}

a {
    text-decoration: none;
    display: flex;
}

.tweet_text_container {
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