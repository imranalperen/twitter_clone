<template>
<div class="main_trends">
    <div class="title">
        <h1>Trends</h1>
    </div>
    <div class="trends">
        <div class="trend" v-for="tag in tags" @click="redirect_topic(tag[0])">
            <p class="trend_title">{{ tag[0] }}</p>
            <p class="trend_tweet">{{ tag[1] }} Tweets</p>
        </div>
    </div>
</div>
</template>

<script>
import { trend_topics_request } from "@/requests"

export default {
    data() {
        return {
            tags: null
        }
    },

    async beforeCreate(){
        this.tags = await trend_topics_request()
        this.tags = this.tags.response
    },

    methods: {
        redirect_topic(topic) {
            topic = topic.split('#')[1]
            this.$router.push({ name: 'topic', params: { string: `${topic}` } })
        }
    }
}
</script>

<style scoped>
.main_trends {
    background-color: var(--thirdBG);
    margin-top: .5em;
    padding: 1em 0 1.4em 0;
    border-radius: 25px;
}

h1 {
    font-size: 1.4em;
    padding-left: .6em;
}

.trend {
    padding: .5em 0 .5em 0;
    cursor: pointer;
    padding-left: 1em;
}

.trend_title {
    font-weight: 500;
}

.trend_tweet {
    font-size: .85em;
    color: var(--gray);
    margin-top: .1em;
}

.trend:hover {
    background-color: var(--itemBackground);
    transition: .3s;
}

</style>