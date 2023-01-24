<template>
<div class="explore_page_general" v-if="tweets">
    <tweet_container
        :user="user"
        :tweets="tweets"
    />
</div>
</template>


<script>
import { explore_timeline_request } from '@/requests'
import tweet_container from '@/components/main/tweet_container.vue'

export default {
    components: {
        tweet_container
    },

    props: ["user"],

    data() {
        return {
            tweets: null
        }
    },

    async beforeCreate() {
        let response_value = await explore_timeline_request()
        this.tweets = response_value.response
    }
}

</script>

<style scoped>

</style>