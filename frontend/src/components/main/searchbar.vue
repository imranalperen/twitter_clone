<template>
<div class="main_searchbar">
    <div class="input">
        <input id="searchbar_input" type="text" placeholder="Search Clone" v-model="keyword" @input="search">
    </div>
    <div class="results">
        <div class="user">
            <div class="user_image_container">
                image
            </div>
            <div class="name_container">
                <div class="name">
                    <p class="name_text">imran alperen bayram</p>
                </div>
                <div class="username">
                    <p class="username_text">@alperen</p>
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
            this.users = await search_users_request(this.keyword)
            console.log(this.users)
        }
    }
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
    border-left: 1px solid var(--bordergray);
    border-right: 1px solid var(--bordergray);
    border-bottom: 1px solid var(--bordergray);
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    padding: 1em;
}

.user {
    display: flex;
    flex-direction: row;
}

.name_container {
    display: flex;
    flex-direction: column;
}

</style>