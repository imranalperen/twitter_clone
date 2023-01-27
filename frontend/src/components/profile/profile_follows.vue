<template>
<div class="profile_follows_general">
    <div class="close_modal">
        <img id="clear_image_btn" src="@/assets/icons8-xbox-x-50.png" @click="this.$emit('toggle_modal_bool')">
    </div>
    <div class="follows_header">
        <h1>Follows</h1>
    </div>
    <div class="follow_users" v-if="following_users != ''">
        <div class="user" v-for="user in following_users" :key="user.id">
            <div class="left">
                <div class="image">
                    <img :src="user.image">
                </div>
                <div class="names">
                    <p class="name">{{ user.name }}</p>
                    <p class="username">@{{ user.username }}</p>
                </div>
            </div>
            <div class="right" v-if="user.id != visitor_user.id">
                <div class="follow_btn_container">
                    <button
                        class="follow_btn"
                        v-if="user.is_following == false"
                        @click="follow_user_request(user)"
                    >follow</button>
                    <button
                        class="unfollow_btn"
                        v-else
                        @click="unfollow_user_request(user)"
                    >Following</button>
                </div>
            </div>
        </div>
    </div>
    <div v-else>
        <p class="three_dots">...</p>
    </div>
</div>
</template>

<script>
import { user_follows_request } from '@/requests'
import { follow_request, unfollow_request } from "@/requests"
export default {
    props: ["visited_user", "visitor_user", "purpose"],

    emits: ["toggle_modal_bool"],

    data() {
        return {
            following_users: null,
        }
    },

    async beforeCreate() {
        this.following_users = await user_follows_request(this.visited_user.user_id, this.purpose)
        this.following_users = this.following_users.response
    },

    methods: {
        async follow_user_request(user) {
            let response = await follow_request(user.id)
            if(response) {
                user.is_following = true
            }
        },

        async unfollow_user_request(user) {
            let response = await unfollow_request(user.id)
            if(response) {
                user.is_following = false
            }
        }
    }
}
</script>

<style scoped>
.profile_follows_general {
    background-color: var(--primaryBG);
    max-height: 80vh;
    padding: 1em 2em 0 2em;
    overflow: scroll;
    border-radius: 25px;
}

.close_modal > img {
    width: 35px;
    filter: invert(99%) sepia(55%) saturate(453%) hue-rotate(256deg) brightness(122%) contrast(87%);
    cursor: pointer;
}

.follows_header > h1 {
    display: flex;
    justify-content: center;
    letter-spacing: 1px;
    border-bottom: 1px solid var(--bordergray);
    padding-bottom: .3em;
    margin-bottom: .3em;
}
 
.user {
    /* display: flex;
    flex-direction: row;
    padding: .5em; */
    display: grid;
    grid-template-columns: 1fr .3fr;
    padding: .5em;
}

.left {
    display: flex;
    flex-direction: row;
}

.image > img {
    border-radius: 50%;
    width: 55px;
    height: 55px;
    border: 1px solid white; /*! DEVELOPMENT DELETE WHEN PAGE COMPLETED */
}

.names {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-left: .5em;
}

.right {
    display: flex;
    align-items: center;
}

.follow_btn {
    margin: .5em 0 .5em .4em;
    color: black;
    background-color: white;
    border-style: none;
    padding: .5em .8em .5em .8em;
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
    padding: .5em .8em .5em .8em;
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
}

.three_dots {
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: bold;
    font-size: 3em;
    color: var(--gray);
    letter-spacing: 2px;
    padding: 1em 2em 2em 2em;
}

</style>