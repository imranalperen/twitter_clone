<template>
<div class="main_who_to_follow">
    <div class="title">
        <h1>Who to follow</h1>
    </div>
    <div class="profile">
        <div class="left">
            <div class="image">
                <img src="@/assets/depositphotos_137014128-stock-illustration-user-profile-icon.jpg">
            </div>
            <div class="names">
                <p class="name">fake1</p>
                <p class="username">@fakeuser1</p>
            </div>
        </div>
        <div class="right">
            <div class="follow_btn_container">
                <button class="follow_btn">Follow</button>
            </div>
        </div>
    </div>
    <div class="profile">
        <div class="left">
            <div class="image">
                <img src="@/assets/depositphotos_137014128-stock-illustration-user-profile-icon.jpg">
            </div>
            <div class="names">
                <p class="name">fake1</p>
                <p class="username">@fakeuser1</p>
            </div>
        </div>
        <div class="right">
            <div class="follow_btn_container">
                <button class="following_btn">Following</button>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import { recommend_user_request } from "@/requests"

export default {
    data() {
        return {
            recommend_user_list: [],
        }
    },

    async beforeCreate() {
        //we will recommedn 2 user which main user doesnt follow
        this.recommend_user_list = await recommend_user_request()
        console.log(this.recommend_user_list)
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

.image > img {
    width: 50px;
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

.following_btn {
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

.following_btn:hover {
    color: crimson;
    border-color: crimson;
    background-color: rgba(220, 20, 60, .2);
}
</style>