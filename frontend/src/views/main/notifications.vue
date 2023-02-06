<template>
<div class="notifications_general_container">
    <div class="notification_bar" v-for="notification in notifications_data">
        <div class="profile_image_container">
            <img :src="notification.profile_image" class="profile_image">
            <div class="notification" v-if="notification.event == 'like'">
                <p>{{ notification.username }} liked your tweet.</p>
            </div>
            <div class="notification" v-if="notification.event == 'reply'">
                <p>{{ notification.username }} replied your tweet.</p>
            </div>
            <div class="notification" v-if="notification.event == 'retweet'">
                <p>{{ notification.username }} retweet your tweet.</p>
            </div>
        </div>
        <router-link :to="{name: 'tweet_page', params:{id: notification.tweet_id}}" class="r_link">
            <div class="notifications_text_container">
                <p class="preview_tweet" v-if="notification.tweet_body">{{ notification.tweet_body }}</p>
                <img v-if="notification.tweet_image" :src="notification.tweet_image" class="preview_tweet_image">
            </div>
        </router-link>
    </div>
</div>
</template>

<script>
import {mark_as_read_notifications_request, notifications_request} from '@/requests'

export default {
    props: ["user", "notifications_response"],

    data() {
        return {
            notifications_data: null
        }
    },

    async beforeCreate() {
        this.notifications_data = await notifications_request()
        this.notifications_data = this.notifications_data.response

        await mark_as_read_notifications_request()
    }
}

</script>

<style scoped>
.notifications_general_container {
    display: flex;
    flex-direction: column;
}
.notification_bar {
    display: flex;
    flex-direction: column;
    padding: .5em;
    border-top: 1px solid var(--bordergray);
}

.profile_image {
    width: 60px;
    height: 60px;
    border-radius: 50%;
}

.profile_image_container {
    display: flex;
    gap: 1em;
    align-items: center;
    padding-bottom: 1em;
}

.notifications_text_container {
    border: 1px solid var(--bordergray);
    padding: 0 1em 0 1em;
    border-radius: 15px;
    cursor: pointer;
}

.preview_tweet {
    padding: 1em;
}

.preview_tweet_image {
    max-width: 250px;
    max-height: 250px;
    padding: 1em;
    border-radius: 25px;
}

.notifications_text_container:hover {
    background-color: var(--itemBackground);
    transition: .2s;
}

.r_link {
    text-decoration: none;
}
</style>