<template>
    <div class="tweet_page_general_container">

    </div>
</template>

<script>
import { tweet_page_request } from '@/requests'
export default {
    data() {
        return {
            parent_tweet: [],
            child_tweets: []
        }
    },

    async beforeCreate() {
        let tweet_id = this.$route.fullPath.split("/")[2]
        let request_body = {"tweet_id": tweet_id}
        let response_value = await tweet_page_request(request_body)
        this.parent_tweet = response_value.response.parent_tweet
        this.child_tweets = response_value.response.child_tweets
        console.log(this.child_tweets)
        console.log(this.parent_tweet)
    }
}
</script>

<style>

</style>