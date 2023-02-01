<template>
<div class="profile_page_general_container" v-if="visited_user">
    <div class="top_container">
        <div class="profile_image_container">
            <img :src="visited_user.profile_image">
        </div>
        <div class="buttons_container">
            <div class="dm_container" v-if="visited_user.following_situation != 'edit_profile'">
                <router-link :to="{name: 'message_page', params:{target_username: visited_user.username}}">
                <img src="@/assets/mail-outline.svg" class="message_image">
                </router-link>
            </div>
            <div class="follow_container">
                <button
                    v-if="visited_user.following_situation == 'edit_profile'"
                    class="follow_btn"
                    @click="toggle_edit_profile()"
                >Edit Profile</button>
                <button
                    v-if="visited_user.following_situation == 'follow'"
                    @click="follow_user_request(visited_user.user_id)"
                    class="follow_btn"
                >follow</button>
                <button
                    v-if="visited_user.following_situation == 'unfollow'"
                    @click="unfollow_user_request(visited_user.user_id)"
                    class="unfollow_btn"
                >unfollow</button>
            </div>
        </div>
    </div>
    <div class="user_informations">
        <div class="name_container">
            <p>{{ visited_user.name }}</p>
        </div>
        <div class="username_container">
            <p class="gray_text">@{{ visited_user.username }}</p>
        </div>
        <div class="bio_container">
            <p class="biography">{{ visited_user.biography }}</p>
        </div>
        <div class="follow_and_followers_container">
            <div class="follows_container" @click="toggle_follows()">
                <p class="number">{{ visited_user.follow_count }}</p>
                <p class="gray_text small_text">Following</p>
            </div>
            <div class="followers_container" @click="toggle_followers()">
                <p class="number right_number">{{ visited_user.followers_count }}</p>
                <p class="gray_text small_text">Followers</p>
            </div>
        </div>
    </div>
    <div class="headers_container">
        <router-link
            :to="{name: 'profile', params: {string: visited_user.username, profile_tab: null}}"
            class="header"
            :class="{selected_header: tab_name == null}">
                <p>Tweets</p>
        </router-link>

        <router-link
            :to="{name: 'profile', params: {string: visited_user.username, profile_tab: 'media'}}"
            class="header"
            :class="{selected_header: tab_name == 'media'}">
                <p>Media</p>
        </router-link>

        <router-link
            :to="{name: 'profile', params: {string: visited_user.username, profile_tab: 'likes'}}"
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

    <div class="modal_container" v-if="modal_bool">
        <div class="sticky_container">
            <div v-if="active_modal == 'edit_profile'" class="sticky_modal">
                <edit_profile
                    :visited_user = visited_user
                    @toggle_modal_bool = toggle_modal_bool()
                />
            </div>
            <div v-if="active_modal == 'follows'" class="sticky_modal">
                <profile_follows
                    :visitor_user="user"
                    :visited_user = visited_user
                    :purpose="'follows'"
                    @toggle_modal_bool = toggle_modal_bool()
                />
            </div>
            <div v-if="active_modal == 'followers'" class="sticky_modal">
                <profile_follows
                    :visitor_user="user"
                    :visited_user = visited_user
                    :purpose="'followers'"
                    @toggle_modal_bool = toggle_modal_bool()
                />
            </div>
        </div>
    </div>
</div>
</template>

<script>
import {
    profile_request,
    profile_tweets_request,
} from '@/requests'

import tweet_container from '@/components/main/tweet_container.vue'
import edit_profile from '@/components/profile/edit_profile.vue'
import profile_follows from '@/components/profile/profile_follows.vue'
import { follow_request, unfollow_request } from "@/requests"

export default {
    props: ["user"],

    components: {
        tweet_container,
        edit_profile,
        profile_follows,
    },

    data() {
        return {
            visited_user: null,
            tab_name: null,
            tweets: null,
            modal_bool: false,
            active_modal: ''
        }
    },

    async beforeCreate() {
        //we cant use props in beforecreate hook so we get username from url
        //username is unique name is not unique
        let username = this.$route.fullPath.split('/')[2]
        let response_value = await profile_request(username)
        this.visited_user = response_value.response[0]
        this.tab_name = this.$route.fullPath.split('/')[3]
    },

    methods: {
        async follow_user_request(user_id) {
            let response = await follow_request(user_id)
            if(response) {
                this.visited_user.following_situation = "unfollow"
            }
        },

        async unfollow_user_request(user_id) {
            let response = await unfollow_request(user_id)
            if(response) {
                this.visited_user.following_situation = "follow"
            }
        },

        toggle_modal_bool() {
            this.modal_bool = !this.modal_bool
            if (!this.modal_bool) {
                // if(this.active_modal == "edit_profile"){
                //     location.reload()
                // }
                location.reload()
            }
        },

        toggle_edit_profile() {
            this.toggle_modal_bool()
            this.active_modal = "edit_profile"
        },

        toggle_follows() {
            this.toggle_modal_bool()
            this.active_modal = "follows"
        },

        toggle_followers() {
            this.toggle_modal_bool()
            this.active_modal = "followers"
        }
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
                this.tweets = await profile_tweets_request(this.visited_user.username, temp_tab_name)
                this.tweets = this.tweets.response
            }
            else if(this.tab_name == "media") {
                this.tweets = await profile_tweets_request(this.visited_user.username, this.tab_name)
                this.tweets = this.tweets.response
            }
            else if(this.tab_name == "likes") {
                this.tweets = await profile_tweets_request(this.visited_user.username, this.tab_name)
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
/* EDIT PROFILE MODAL */
.modal_container {
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(52, 64, 77, .5);
    z-index: 10;

}

/* PROFILE */
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

.bio_container {
    margin-top: 1.3em;
}

.gray_text {
    color: var(--gray);
}

.small_text {
    font-size: .9em;
    margin-left: .3em;
}

.number {
    font-weight: bold;
}
.right_number {
    margin-left: .5em;
}

.follow_and_followers_container {
    display: flex;
    justify-content: row;
    margin-top: 1em;
}

burada
.followers_container {
    margin-left: 1em;
}

.follows_container, .followers_container {
    display: flex;
    cursor: pointer;
    padding: .3em;
}

a {
    text-decoration: none;
}

.followers_container:hover, .follows_container:hover {
    background-color: var(--bordergray);
    border-radius: 5px;
    transition: .2s;
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