<template>
<div class="menu_container" v-if="user">
    <div class="menu">
        <router-link class="menu_element" :to="{name: 'home'}">
            <img class="hashtag" src="@/assets/icons8-twitter.svg">
        </router-link>

        <router-link class="menu_element" :to="{name: 'home'}">
            <div class="menu_image">
                <img class="icon" src="@/assets/home.svg">
            </div>
            <p class="menu_text">Home</p>
        </router-link>

        <router-link class="menu_element" :to="{name: 'explore'}">
            <div class="menu_image">
                <img class="hashtag" src="@/assets/icons8-hashtag-50.png">
            </div>
            <p class="menu_text">Explore</p>
        </router-link>

        <router-link class="menu_element" :to="{name: 'notifications'}">
            <div class="menu_image">
                <img class="icon" src="@/assets/notifications-outline.svg">
            </div>
            <p class="menu_text">Notifications</p>
        </router-link>

        <router-link class="menu_element" :to="{name: 'messages'}">
            <div class="menu_image">
                <img class="icon" src="@/assets/mail-outline.svg">
            </div>
            <p class="menu_text">Messages</p>
        </router-link>

        <router-link class="menu_element" :to="{name: 'profile', params: {string: `${user.username}`, profile_tab: null}}">
            <div class="menu_image">
                <img class="icon" src="@/assets/person-outline.svg">
            </div>
            <p class="menu_text">Profile</p>
        </router-link>

        <router-link class="menu_element" :to="{name: 'home'}">
            <div class="menu_image">
                <img class="icon" src="@/assets/ellipsis-horizontal-circle-outline.svg">
            </div>
            <p class="menu_text">More</p>
        </router-link>

        <div class="menu_tweet">
            <button id="menu_tweet_btn">Tweet</button>
        </div>
    </div>

    <div class="user_info_bottom" v-if="user">
        <router-link :to="{name: 'profile', params:{string: user.username, profile_tab :null}}" class="r_link">
            <div class="user_info_left">
                <div class="user_info_image">
                    <img :src="user.profile_image" alt="">
                </div>
                <div class="user_info_right">
                    <p id="name">{{ user.name }}</p>
                    <p id="username">@{{ user.username }}</p>
                </div>
            </div>
        </router-link>
        <div class="user_info_right_image" @click="logout">
            <img class="icon" src="@/assets/log-out-outline.svg">
        </div>
    </div>

</div>
</template>


<script>
export default {
    props: ["user"],

    methods: {
        logout() {
            window.localStorage.clear()
            this.$router.push({name: "login"})
        },
        
        push_main() {
            this.$router.push({name: "home"})
        },

        push_explore() {
            this.$router.push({name: "explore"})
        },

        push_profile() {
            this.$router.push({name: "profile", params: { string: `${this.user.username}`}})
        }
    }
}

</script>


<style scoped>
.icon {
    width: 30px;
    filter: invert(100%) sepia(6%) saturate(73%) hue-rotate(193deg) brightness(111%) contrast(87%);
}

.hashtag {
    width: 30px;
}

.menu_container {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.menu {
    padding: .3em 0 .2em 1em;
}

.menu_element {
    display: flex;
    align-items: center;
    padding: .5em 0 .5em .3em;
    cursor: pointer;
    text-decoration: none;
}

.menu_tweet{
    margin-right: 3em;
}

#menu_tweet_btn {
    margin: .5em 0 .5em .4em;
    color: var(--colorWhite);
    background-color: var(--tweetBtnBg);
    border-style: none;
    padding: 1em 2em 1em 2em;
    width: 100%;
    border-radius: 25px;
    font-weight: 500;
    font-size: 1em;
    cursor: pointer;
}

#menu_tweet_btn:hover {
    transition: .1s;
    background-color: var(--tweetBtnDarkBg);
}

.menu_element > p {
    margin-left: 1em;
    font-weight: 500;
}

.menu_element:hover {
    background-color: var(--itemBackground);
    border-radius: 15px;
}

.user_info_bottom {
    display: flex;
    justify-content: space-between;
    padding: .3em .3em .3em .3em;
    margin: .3em 3.3em .6em 1em;
    align-items: center;
}

.user_info_left {
    display: flex;
}

.user_info_image > img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
}

.user_info_right {
    margin-left: .4em;
}

.user_info_right_image > img {
    rotate: 180deg;
    cursor: pointer;
}

#username {
    font-size: .9em;
    margin-top: .3em;
    color: var(--gray);
}

.user_info_bottom:hover {
    background-color: red;
    border-radius: 25px;
    background-color: var(--itemBackground);
}

.r_link {
    text-decoration: none;
}
</style>