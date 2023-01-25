<template>
<div class="profile_page_general_container" v-if="user_infos && user_tweets && user">
    <div class="top_container">
        <div class="profile_image_container">
            <img :src="user_infos.profile_image">
        </div>
        <div class="buttons_container">
            <div class="dm_container">
                <img src="@/assets/mail-outline.svg">
            </div>
            <div class="follow_container">
                <button
                    class="follow_btn"
                >Follow</button>
            </div>
        </div>
    </div>
    <div class="user_informations">
        <div class="name_container">
            <p>imran alperen bayram</p>
        </div>
        <div class="username_container">
            <p class="gray_text">@imranalperen</p>
        </div>
        <div class="follow_and_followers_container">
            <div class="follows_container">
                <a href="">
                    <p class="number">123</p>
                    <p class="gray_text small_text">Following</p>
                </a>
            </div>
            <div class="followers_container">
                <a href="">
                    <p class="number">2</p>
                    <p class="gray_text small_text">Followers</p>
                </a>
            </div>
        </div>
    </div>
    <div class="headers_container">
        <router-link :to="{name: 'profile', params: {string: user.username, profile_tab: null}}" class="header" :class="{selected_header: tab_name == null}">
            <p>Tweets</p>
        </router-link>
        <router-link :to="{name: 'profile', params: {string: user.username, profile_tab: 'replies'}}" class="header" :class="{selected_header: tab_name == 'replies'}">
            <p>Tweets&Replies</p>
        </router-link>
        <router-link :to="{name: 'profile', params: {string: user.username, profile_tab: 'media'}}" class="header" :class="{selected_header: tab_name == 'media'}">
            <p>Media</p>
        </router-link>
        <router-link :to="{name: 'profile', params: {string: user.username, profile_tab: 'likes'}}" class="header" :class="{selected_header: tab_name == 'likes'}">
            <p>Likes</p>
        </router-link>
    </div>
    <div class="profile_tweets_container">

    </div>
</div>
</template>

<script>
import { profile_request } from '@/requests'

export default {
    props: ["user"],

    data() {
        return {
            user_tweets: null,
            user_infos: null,
            tab_name: null
        }
    },

    async beforeCreate() {
        //we cant use props in beforecreate hook so we get username from url
        //username is unique name is not unique
        let username = this.$route.fullPath.split('/')[2]
        let response_value = await profile_request(username)
        this.user_tweets = response_value.user_tweets
        this.user_infos = response_value.user_profile[0]
        this.tab_name = this.$route.fullPath.split('/')[3]
        //create requests according to tab name
    }
}

</script>

<style scoped>
.profile_page_general_container {
    display: flex;
    flex-direction: column;
}

.top_container {
    display: flex;
    justify-content: space-between;
    padding: 0 2em 0 2em;
}

.profile_image_container > img {
    width: 135px;
    height: 135px;
    border-radius: 50%;
}

.buttons_container {
    display: flex;
    align-items: flex-end;
    margin-bottom: 1em;
}

.dm_container > img {
    filter: invert(100%) sepia(6%) saturate(73%) hue-rotate(193deg) brightness(111%) contrast(87%);
    border-radius: 50%;
    width: 43px;
    padding: .5em;
    border: 1px solid var(--bordergray);
    cursor: pointer;
}

.follow_btn {
    margin: .5em 0 .5em .4em;
    color: black;
    background-color: white;
    border-style: none;
    padding: .6em .8em .6em .8em;
    width: 100%;
    border-radius: 25px;
    font-weight: 500;
    font-size: 1em;
    cursor: pointer;
}

.user_informations {
    display: flex;
    flex-direction: column;
    margin-left: 1.3em;
    margin-top: 1em;
}

.name_container > p {
    font-weight: bold;
    font-size: 1.1em;
}

.gray_text {
    color: var(--gray);
}

.small_text {
    font-size: .9em;
}

.number {
    font-weight: bold;
}

.follow_and_followers_container {
    display: flex;
    justify-content: row;
    margin-top: 1em;
}

.follows_container > a, .followers_container > a {
    display: flex;
    justify-content: row;
    gap: .3em;
}

a {
    text-decoration: none;
}
.followers_container {
    margin-left: 1em;
}

.headers_container {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    border-bottom: 1px solid var(--bordergray);
    margin-top: 1em;
}
.header {
    padding: 1em;
    display: flex;
    justify-content: center;
}

.header > p {
    color: var(--gray);
}
.header:hover {
    background-color: var(--bordergray);
    transition: .3s;
}

.selected_header {
    border-bottom: 3px solid var(--tweetBtnBg);
}

.selected_header > p {
    color: white;
}
</style>