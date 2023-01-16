<template>
<div class="home_container">
    <main_tweet
        :user="user"
        @refresh_tweets="add_new_tweet_timeline()"
    />
    <!-- <div class="timeline" v-if="timeline_elements != 2002">
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
                            @add_replied_tweet_timeline = add_new_tweet(tweet.tweet_id)
                        ></reply_tweet>
                    </div>
                </div>
            </div>
        </div>
    </div>


    <div class="timeline" v-else>
        user follows noone recommend users for user 
    </div> -->

    <tweet_container
        :user="user"
        :tweets="timeline_elements"
        @add_new_tweet_timeline_emit = add_new_tweet_timeline()
    />
</div>
</template>

<script>
import main_tweet from '@/components/main/main_tweet.vue'
import reply_tweet from '@/components/main/reply_tweet.vue'
import tweet_container from '@/components/main/tweet_container.vue'

import {
    timeline_request,
    like_request,
    unlike_request,
    retweet_request,
    unretweet_request,
    last_tweet_of_user_request,
} from '@/requests'


export default {
    components: {
        main_tweet,
        reply_tweet,
        tweet_container
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

    },

    methods: {

        // toggle_reply_container(tweet_id) {
        //     if(this.toggle_reply_id) {
        //         this.toggle_reply_id = null
        //     }
        //     else {
        //         this.toggle_reply_id = tweet_id
        //     }
        // },

        async add_new_tweet_timeline() {
            let new_tweet_object = await last_tweet_of_user_request()
            this.timeline_elements = [new_tweet_object.response[0]].concat(this.timeline_elements)
            // if(replied_twet_id) {
            //     for(let i = 0; i < this.timeline_elements.length; i++) {
            //         if(this.timeline_elements[i].tweet_id == replied_twet_id) {
            //             this.timeline_elements[i].reply_count += 1
            //             this.toggle_reply_container(replied_twet_id)
            //         }
            //     }
            // }
        },

    },
}

</script>

<style scoped>
</style>