<template>
<div class="profile_page_general_container">
    
</div>
</template>

<script>
import { user_tweets_request } from '@/requests'

export default {
    props: ["user"],

    data() {
        return {
            user_tweets: null,
        }
    },

    async beforeCreate() {
        //we cant use props in beforecreate hook so we get username from url
        //username is unique name is not unique
        let username = this.$route.fullPath.split('/')[2]
        this.user_tweets = await user_tweets_request(username)
        console.log(this.user_tweets.response)
    }
}

</script>

<style scoped>

</style>