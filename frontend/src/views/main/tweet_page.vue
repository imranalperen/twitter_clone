<template>
    <!-- TODO tweet page restructure -->
<div class="tweet_page_general_container">
    tweet page

</div>
</template>

<script>
import { tweet_page_request } from '@/requests'
import tweet_container from '@/components/main/tweet_container.vue'

export default {
    components: {
        tweet_container
    },

    props: ["user"],

    data() {
        return {
            parent_tweet: null,
            replied_tweet: null,
            child_tweets: null
        }
    },

    async beforeCreate() {
        let tweet_id = this.$route.fullPath.split("/")[2]
        let request_body = {"tweet_id": tweet_id}
        let response_value = await tweet_page_request(request_body)
        console.log(response_value)
        // this.parent_tweet = response_value.response.parent_tweet[0]
        // this.replied_tweet = response_value.response.replied_tweet[0]
        // this.child_tweets = response_value.response.child_tweets
        console.log("parent tweet: ", this.parent_tweet)
        console.log("reply tweet: ", this.replied_tweet)
        console.log("child tweets: ", this.child_tweets)
    },

    methods: {

    },
}
</script>

<style scoped>
.seperator {
    border-bottom: 1px solid var(--bordergray);
}

.seperator > p {
    text-align: center;
    font-size: 1.2em;
    padding: .4em;
    color: var(--bordergray);
    font-weight: bold;
}
</style>