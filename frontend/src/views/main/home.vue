<template>
<div class="home_container">
    <main_tweet
        :user="user"
        @refresh_tweets="add_new_tweet_timeline()"
    />

    <tweet_container
        :user="user"
        :tweets="timeline_elements"
        @add_new_tweet_timeline_emit = "add_new_tweet_timeline()"
    />
</div>
</template>

<script>
import main_tweet from '@/components/main/main_tweet.vue'
import reply_tweet from '@/components/main/reply_tweet.vue'
import tweet_container from '@/components/main/tweet_container.vue'

import {
    timeline_request,
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
        async add_new_tweet_timeline() {
            let new_tweet_object = await last_tweet_of_user_request()
            this.timeline_elements = [new_tweet_object.response[0]].concat(this.timeline_elements)
        },

    },
}

</script>

<style scoped>
</style>