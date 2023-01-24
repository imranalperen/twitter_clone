<template>
    <!-- TODO tweet page restructure -->
<div class="tweet_page_general_container">
    <div class="parent_tweet_container">
        <tweet_container
            :user="user"
            :tweets="parent_tweet"
            @add_new_tweet_timeline_emit = "reload_page()"
        />
    </div>
    <div class="seperator">
        <p>Replies</p>
    </div>
    <div class="child_tweets_container">
        <tweet_container
            :user="user"
            :tweets="child_tweets"
        />
    </div>

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
            parent_tweet: [],
            child_tweets: [],
            url: null
        }
    },

    async beforeCreate() {
        let tweet_id = this.$route.fullPath.split("/")[2]
        this.url = this.$route.fullPath
        let request_body = {"tweet_id": tweet_id}
        let response_value = await tweet_page_request(request_body)
        this.parent_tweet = response_value.response.parent_tweet
        this.child_tweets = response_value.response.child_tweets
    },

    methods: {
        reload_page() {
            location.reload()
        }
    },
    
    watch: {
        $route(to, from) {
            if(to != from) {
                //when we click a twet from tweet page url will changeb ut page will be keep
                //before_create outputs. to change it we need a new request
                //and easiest way to do this reload page
                location.reload()
            }
        }
    }
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