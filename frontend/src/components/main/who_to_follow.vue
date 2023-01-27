<template>
<div class="main_who_to_follow" v-if="recommend_user_list">
    <div class="title">
        <h1>Who to follow</h1>
    </div>
    <div class="profile" v-for="user in recommend_user_list">
        <div class="left">
            <div class="image">
                <!-- <img :src="user.image"> -->
                <router-link :to="{name: 'profile', params:{string: user.username, profile_tab :null}}" class="r_link">
                    <img class="profile_image" :src="user.image">
                </router-link>
            </div>
            <div class="names">
                <router-link :to="{name: 'profile', params:{string: user.username, profile_tab :null}}" class="r_link">
                    <p class="name">{{ user.name }}</p>
                    <p class="username">@{{ user.username }}</p>
                </router-link>
            </div>
        </div>
        <div class="right">
            <div class="follow_btn_container">
                <button
                    class="follow_btn"
                    v-if="user.is_following == false"
                    @click="follow_user_request(user)"
                >Follow</button>
                
                <button
                    class="unfollow_btn"
                    v-else
                    @click="unfollow_user_request(user)"
                >Following</button>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import { recommend_user_request, follow_request, unfollow_request } from "@/requests"

export default {
    data() {
        return {
            recommend_user_list: [],
        }
    },

    async beforeCreate() {
        //we will recommedn 2 user which main user doesnt follow
        this.recommend_user_list = await recommend_user_request()
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
.main_who_to_follow {
    background-color: var(--thirdBG);
    margin-top: 1em;
    padding: 1em 0 1.4em 0;
    border-radius: 25px;
}

h1 {
    font-size: 1.4em;
    padding-left: .6em;
}

.profile_image{
    width: 50px;
    height: 50px;
    border-radius: 50%;
}
.profile {
    padding: .5em 0 .5em 0;
    cursor: pointer;
    padding-left: 1em;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.profile:hover {
    background-color: var(--itemBackground);
    transition: .3s;
}

.left {
    display: flex;
    align-items: center;
}

.names {
    margin-left: .5em;
}

.name {
    font-weight: 500;
}

.username {
    font-size: .9em;
    margin-top: .3em;
    color: var(--gray);
}

.right {
    margin-right: 1.5em;
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
    font-size: .8em;
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
    font-size: .8em;
    cursor: pointer;
}

.unfollow_btn:hover {
    color: crimson;
    border-color: crimson;
    background-color: rgba(220, 20, 60, .2);
}

.r_link {
    text-decoration: none;
}
</style>