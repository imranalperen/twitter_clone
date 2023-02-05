<template>
    <!-- TODO tweet page restructure -->
<div class="tweet_page_general_container">
    <div class="repliy_and_parent_wrapper">
        <div class="parent_tweet">
            <tweet_container
                :user="user"
                :tweets="parent_tweet"
                @add_new_tweet_timeline_emit = "add_new_tweet_timeline()"
                :is_big="true"
                :is_parent="is_parent"
            />
        </div>
        <!-- <div class="vertical"></div> -->
        <div class="reply_tweet" v-if="replied_tweet">
            <tweet_container
                :user="user"
                :tweets="replied_tweet"
                @add_new_tweet_timeline_emit = "add_new_tweet_timeline()"
                :is_big="true"
                :is_tweet_page_reply = "true"
            />
        </div>
    </div>
    <div class="replies_title"><p class="replies">Replies</p></div>
    <div class="child_tweets" v-if="child_tweets">
        <tweet_container
            :user="user"
            :tweets="child_tweets"
        />
    </div>
</div>
</template>

<script>
import { tweet_page_request, last_reply_of_tweet_request } from '@/requests'
import tweet_container from '@/components/main/tweet_container.vue'
import css_test from '@/components/css_test.vue'

export default {
    components: {
        tweet_container,
        css_test
    },

    props: ["user"],

    data() {
        return {
            parent_tweet: null,
            replied_tweet: null,
            child_tweets: null,
            is_parent: false,
        }
    },

    async beforeCreate() {
        let tweet_id = this.$route.fullPath.split("/")[2]
        let request_body = {"tweet_id": tweet_id}
        let response_value = await tweet_page_request(request_body)
        this.parent_tweet = response_value.response.parent_tweet
        this.replied_tweet = response_value.response.replied_tweet
        this.child_tweets = response_value.response.child_tweets
        if (this.replied_tweet != '') {
            this.is_parent = true
        }
    },

    methods: {
        async add_new_tweet_timeline() {
            // let new_tweet_object = await last_tweet_of_user_request()
            // this.timeline_elements = [new_tweet_object.response[0]].concat(this.timeline_elements)
            const tweet_id = this.$route.fullPath.split("/")[2]
            let new_tweet_object = await last_reply_of_tweet_request(tweet_id)
            // console.log(new_tweet_object.response.tweet[0])
            this.child_tweets = [new_tweet_object.response.tweet[0]].concat(this.child_tweets)
        }
    },
}
</script>

<style scoped>
.replies_title {
    text-align: center;
    border-bottom: 1px solid var(--bordergray);
    border-top: 1px solid var(--bordergray);;
    padding: .6em;
}

.replies {
    color: var(--gray);
    font-weight: bold;
    font-size: 1.2em;
    letter-spacing: 1px;
}

/* .repliy_and_parent_wrapper {
    display: flex;
    flex-direction: column;
} */

/* .vertical {
    border-left: 5px solid white;
    position: absolute;
    margin-left: 3em;
    top: 5em;
    bottom: 1em;
} */
</style>