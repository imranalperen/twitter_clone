<template>
<div class="main_searchbar">
    <div class="input">
        <input
            id="searchbar_input"
            type="text"
            placeholder="Search Clone"
            v-model="keyword"
            @input="search"
            @focusout="clear_users"
        >
    </div>
    <div class="results" v-if="users">
        <div class="user" v-for="user in users" @click="redirect_user_profile(user.username)">
            <div class="user_image_container">
                <img :src="user.profile_image" class="profile_image">
            </div>
            <div class="name_container">
                <div class="name">
                    <p class="name_text">{{ user.name }}</p>
                </div>
                <div class="username">
                    <p class="username_text">@{{ user.username }}</p>
                </div>
            </div>
        </div>
    </div>
</div>
</template>


<script>
import {search_users_request} from '@/requests'
export default {
    data() {
        return {
            keyword: '',
            users: null,
            filtered_users: null,
        }
    },

    methods: {
        async search() {
            if(this.keyword == '') {
                this.users = null
            }
            else {
                this.users = await search_users_request(this.keyword)
                this.users = this.users.response
            }
        },

        redirect_user_profile(username) {
            this.$router.push({name: 'profile', params: {string: `${username}`, profile_tab: null}})
        },

        clear_users() {
            setTimeout(this.clear_users_endpoint, 500)
        },

        clear_users_endpoint() {
            this.users = null
            this.keyword = ''
        },
    },
}

</script>


<style scoped>
.main_searchbar {
    padding-bottom: .5em;
    background-color: rgba(21, 32, 43, .9);
}

#searchbar_input {
    background-color: var(--searchbarBG);
    border-style: none;
    padding: .7em;
    font-size: 1em;
    border-radius: 25px;
    margin-top: .3em;
    width: 100%;
    text-indent: 10px;
    outline: none;
}

::placeholder {
    color: var(--gray);
    font-size: 1em;
    font-weight: 300;
}

#searchbar_input:focus::placeholder {
  color: transparent;
}

.results {
    z-index: 3;
    position: absolute;
    width: 100%;
    background-color: var(--primaryBG);
    max-height: 50vh;
    overflow: scroll;
    overflow-x: hidden;
    border-left: 1px solid var(--bordergray);
    border-right: 1px solid var(--bordergray);
    border-bottom: 1px solid var(--bordergray);
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
}
::-webkit-scrollbar {
  width: 10px;
}

/* Track */
::-webkit-scrollbar-track {
  background: var(--itemBackground); 
}
 
/* Handle */
::-webkit-scrollbar-thumb {
  background: #888; 
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555; 
}

.user {
    display: flex;
    flex-direction: row;
    padding: .4em 1em .4em 1em;
    cursor: pointer;
}

.user:hover {
    background-color: var(--itemBackground);
}

.name_container {
    display: flex;
    flex-direction: column;
    padding-left: .5em;
}

.profile_image {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 1px solid white;
}

.username_text {
    color: var(--gray);
}

</style>