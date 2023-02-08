<template>
<div class="header_main">
    {{ calculate_goback }}
    <div class="go_back" v-if="goback">
        <img src="@/assets/icons8-left-arrow-60.png" @click="go_previus_page">
    </div>
    <div class="header_title" v-if="current_url != 'message_page'">
        <h1 v-if="current_url == 'home'">Home</h1>
        <h1 v-if="current_url == 'tweet_page'">Tweet</h1>
        <h1 v-if="current_url == 'topic'">{{ get_topic }}</h1>
        <h1 v-if="current_url == 'explore'">Explore</h1>
        <h1 v-if="current_url == 'messages'">Messages</h1>
        <h1 v-if="current_url == 'notifications'">Notifications</h1>
    </div>
</div>
</template>

<script>
export default {
    props: ["current_url"],

    data() {
        return {
            goback: false,
            target_username: null,
            target_profile_image: null
        }
    },

    methods: {
        go_previus_page() {
            this.$router.go(-1)
        },
    },

    computed: {
        calculate_goback() {
            if(this.current_url == 'tweet_page' || this.current_url == 'topic') {
                this.goback = true
            }
            else {
                this.goback = false
            }
        },

        get_topic() {
            return this.$route.fullPath.split("/")[2]
        }
    }
}
</script>

<style scoped>
.header_main {
    display: flex;
    width: 100%;
    background-color: rgba(21, 32, 43, .9);
}

.go_back > img {
    filter: invert(100%) sepia(9%) saturate(13%) hue-rotate(247deg) brightness(112%) contrast(87%);
    width: 25px;
    margin-top: .6em;
    margin-left: .3em;
    cursor: pointer;
}
.header_title {
    padding: .5em 0 1.2em 1em;
}

h1 {
    font-size: 1.3em;
    font-weight: 400;
    cursor: pointer;
}

</style>