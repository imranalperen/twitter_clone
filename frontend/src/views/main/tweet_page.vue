<template>
    <div class="tweet_page_general_container">
        
    </div>
</template>

<script>
import { tweet_page_request } from '@/requests'
export default{
    data() {
        return {
            tweet_id: null
        }
    },
    
    async beforeCreate() {
        let url_param = await this.$route.fullPath.split("/")[2]
        this.tweet_id = url_param

        let requst_body = {
            "tweet_id": url_param
        }
        response_value = await tweet_page_request(requst_body)
    }
}
</script>

<style>

</style>