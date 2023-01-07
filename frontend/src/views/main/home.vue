<template>
<div class="home_container">
    <div class="tweet_container">
        <main_tweet
            :user="user"
        />
    </div>
    <div class="timeline" v-if="timeline_elements != 2002">
        timeline elements
        <div v-for="tweet in timeline_elements">
            {{ tweet.user_id }}
            {{ tweet.tweet_id }}
            {{ tweet.name }}
            {{ tweet.username }}
            {{ tweet.time_created }}
            {{ tweet.body }}
            <!-- <img :src="tweet.image"> -->
            =====================================================================
        </div>
    </div> 
    <div class="timeline" v-else>
        user follows noone recommend users for user 
    </div>
</div>
</template>

<script>
import main_tweet from '@/components/main/main_tweet.vue'

import { timeline_request } from '@/requests'

export default {
    components: {
        main_tweet
    },

    props: ["user"],

    data() {
        return {
            timeline_elements: [],
        }
    },

    async beforeCreate() {
        let response_value = await timeline_request()
        this.timeline_elements = response_value.response
    }
}

</script>

<style scoped>


</style>