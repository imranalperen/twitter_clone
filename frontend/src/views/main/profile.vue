<template>
<div class="profile_page_general_container" v-if="user_infos">
    <div class="top_container">
        <div class="profile_image_container">
            <img :src="user_infos.profile_image">
        </div>
        <div class="buttons_container">
            <div class="dm_container">
                <img src="@/assets/mail-outline.svg" class="message_image">
            </div>
            <div class="follow_container">
                
                <div
                    v-if="user_infos.following_situation == 'settings'"
                    class="settings_btn"
                >
                    <img src="@/assets/icons8-settings-50.png" class="settings_image">
                </div>
                    
                

                <button
                    v-if="user_infos.following_situation == 'follow'"
                    class="follow_btn"
                >follow</button>

                <button
                    v-if="user_infos.following_situation == 'unfollow'"
                    class="unfollow_btn"
                >unfollow</button>
            </div>
        </div>
    </div>
    <div class="user_informations">
        <div class="name_container">
            <p>{{ user_infos.name }}</p>
        </div>
        <div class="username_container">
            <p class="gray_text">@{{ user_infos.username }}</p>
        </div>
        <div class="follow_and_followers_container">
            <div class="follows_container">
                <a href="">
                    <p class="number">{{ user_infos.follow_count }}</p>
                    <p class="gray_text small_text">Following</p>
                </a>
            </div>
            <div class="followers_container">
                <a href="">
                    <p class="number">{{ user_infos.followers_count }}</p>
                    <p class="gray_text small_text">Followers</p>
                </a>
            </div>
        </div>
    </div>
    <div class="headers_container">
        <router-link
            :to="{name: 'profile', params: {string: user_infos.username, profile_tab: null}}"
            class="header"
            :class="{selected_header: tab_name == null}">
                <p>Tweets</p>
        </router-link>

        <router-link
            :to="{name: 'profile', params: {string: user_infos.username, profile_tab: 'media'}}"
            class="header"
            :class="{selected_header: tab_name == 'media'}">
                <p>Media</p>
        </router-link>

        <router-link
            :to="{name: 'profile', params: {string: user_infos.username, profile_tab: 'likes'}}"
            class="header"
            :class="{selected_header: tab_name == 'likes'}">
                <p>Likes</p>
        </router-link>
    </div>
    <div class="profile_tweets_container" v-if="tab_request">
        <tweet_container
            :user="user"
            :tweets="tweets"
        />
    </div>
</div>
</template>
    
<script>
import {
    profile_request,
    profile_tweets_request,
} from '@/requests'

import tweet_container from '@/components/main/tweet_container.vue'

export default {
    props: ["user"],

    components: {
        tweet_container
    },

    data() {
        return {
            user_infos: null,
            tab_name: null,
            tweets: null
        }
    },

    async beforeCreate() {
        //we cant use props in beforecreate hook so we get username from url
        //username is unique name is not unique
        let username = this.$route.fullPath.split('/')[2]
        let response_value = await profile_request(username)
        this.user_infos = response_value.response[0]
        this.tab_name = this.$route.fullPath.split('/')[3]
    },
    watch: {
        $route(to, from) {
            if(to != from) {
                this.tab_name = this.$route.fullPath.split('/')[3]
            }
        }
    },

    computed: {
        async tab_request() {
            this.tweets = null
            if(!this.tab_name) {
                //if there is no tab at url this is tweets request
                let temp_tab_name = "tweets"
                this.tweets = await profile_tweets_request(this.user_infos.username, temp_tab_name)
                this.tweets = this.tweets.response
            }
            else if(this.tab_name == "media") {
                this.tweets = await profile_tweets_request(this.user_infos.username, this.tab_name)
                this.tweets = this.tweets.response
            }
            else if(this.tab_name == "likes") {
                this.tweets = await profile_tweets_request(this.user_infos.username, this.tab_name)
                this.tweets = this.tweets.response
            }
            else {
                console.log("patlar")
            }
        }
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
    border: 1px solid white;
}

.buttons_container {
    display: flex;
    align-items: flex-end;
    margin-bottom: 1em;
}

.message_image {
    filter: invert(100%) sepia(6%) saturate(73%) hue-rotate(193deg) brightness(111%) contrast(87%);
    border-radius: 50%;
    width: 43px;
    padding: .5em;
    border: 1px solid var(--bordergray);
    cursor: pointer;
}

.message_image:hover { 
    background-color: var(--tweetBtnBg);
    transition: .3s;
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

.unfollow_btn {
    margin: .5em 0 .5em .4em;
    color: white;
    background-color: var(--thirdBG);
    border-style: none;
    border: 1px solid var(--gray);
    padding: .6em .8em .6em .8em;
    width: 100%;
    border-radius: 25px;
    font-weight: 500;
    font-size: 1em;
    cursor: pointer;
}

.unfollow_btn:hover {
    color: crimson;
    border-color: crimson;
    background-color: rgba(220, 20, 60, .2);
    transition: .3s;
}

.settings_image {
    filter: invert(100%) sepia(6%) saturate(73%) hue-rotate(193deg) brightness(111%) contrast(87%);
    border-radius: 50%;
    width: 43px;
    padding: .5em;
    border: 1px solid var(--bordergray);
    cursor: pointer;
    margin-left: 1em;
}

.settings_image:hover {
    background-color: var(--gray);
}

/* .settings_btn {
    background-color: var(--primaryBG);
    box-shadow: none;
    border-style: none;
    margin-left: 1em;
    border-radius: 50%;
}

.settings_btn > img {
    filter: invert(100%) sepia(6%) saturate(73%) hue-rotate(193deg) brightness(111%) contrast(87%);
    border-radius: 50%;
    width: 43px;
    padding: .5em;
    border: 1px solid var(--bordergray);
    cursor: pointer;
}

.settings_btn:hover {
    filter: invert(100%) sepia(6%) saturate(73%) hue-rotate(193deg) brightness(111%) contrast(87%);
} */

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
    grid-template-columns: 1fr 1fr 1fr;
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