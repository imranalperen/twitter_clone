<template>
<div class="topic_page_general_container" v-if="!tag_feed, load_page">
    <tweet_container
        :user="user"
        :tweets="tag_feed"
    />
</div>
</template>

<script>
import { topic_request } from '@/requests'

import tweet_container from '@/components/main/tweet_container.vue'

export default {
    components: {
        tweet_container
    },

    props: ["user"],

    data() {
        return {
            tag_feed: []
        }
    },
    computed: {
        async load_page() {
            let topic = this.$route.params.string
            this.tag_feed = await topic_request(topic)
            this.tag_feed = this.tag_feed.response
        }
    }
}
</script>

<style scoped>

</style>