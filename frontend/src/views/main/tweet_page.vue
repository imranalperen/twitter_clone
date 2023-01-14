<template>
    <div class="tweet_page_general_container">

    </div>
</template>

<script>
import { tweet_page_request } from '@/requests'
export default {
    data() {
        return {
            
        }
    },

    async beforeCreate() {
        let tweet_id = this.$route.fullPath.split("/")[2]
        let request_body = {"tweet_id": tweet_id}
        let response_value = await tweet_page_request(request_body)
        console.log(response_value.parent_tweet)
        for(let i = 0; i < response_value.child_tweets.length; i++) {
            console.log(response_value.child_tweets[i])
        }
    }
}
</script>

<style>

</style>