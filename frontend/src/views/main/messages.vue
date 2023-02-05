<template>
<div class="messages_list_general_container" v-if="filtered_chat_contacts && main_user">
    <div class="messages_list_search_box">
        <input
            id="search_box"
            type="text"
            placeholder="Search By Username"
            v-model="serach_input"
            @input="filter_chats">
    </div>
    <div class="users_list">
        <div class="user" v-for="chat in filtered_chat_contacts.slice().reverse()" @click="push_message_page(chat.username)" :key="chat.id">
            <div class="left">
                <div class="profile_image_container">
                    <img class="prifle_image" :src="chat.profile_image">
                </div>
            </div>
            <div class="middle">
                <div class="middle_top">
                    <p class="target_name">
                        {{ chat.name }}
                    </p>
                    <p class="target_username">
                        @{{ chat.username }}
                    </p>
                </div>
                <div class="middle_middle">
                    <p class="you" v-if="chat.sender_id == main_user.id">You: </p>
                    <p class="you" v-else>{{ chat.name }}:</p>
                    <p class="message_preview">{{ chat_message_length_calculator(chat.message) }}</p>
                </div>
                <div class="middle_bottom">
                    <p class="date">{{ chat.date }}</p>
                </div>
            </div>
            <div class="right">
                <p class="notification" v-if="chat.message_count">{{ chat.message_count }}</p>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import { chat_contacts_request } from '@/requests'

export default {
    props: ["main_user"],

    data() {
        return {
            chat_contacts: null,
            filtered_chat_contacts: null,
            serach_input: '',
        }
    },

    async beforeCreate() {
        this.chat_contacts = await chat_contacts_request()
        this.chat_contacts = this.chat_contacts.response
        this.filtered_chat_contacts = this.chat_contacts
    },

    methods: {
        push_message_page(username) {
            this.$router.push({name: 'message_page', params:{target_username: username}})
        },

        chat_message_length_calculator(text) {
            if(text.length > 50) {
                text = text.substring(0,50) + '....'
            }
            return text
        },

        filter_chats() {
            if(this.serach_input == '') {
                this.filtered_chat_contacts = this.chat_contacts
            }
            else {
                this.filtered_chat_contacts = this.chat_contacts.filter(chat => {
                    return (chat.username).toLowerCase().includes(this.serach_input.toLowerCase())
                })                
            }
        }
    },

    
}

</script>

<style scoped>
.messages_list_general_container {
    display: flex;
    flex-direction: column;
}
.messages_list_search_box {
    background-color: rgba(21, 32, 43, .9);
        display: flex;
    justify-content: center;
}

#search_box {
    background-color: var(--searchbarBG);
    border-style: none;
    padding: .7em;
    font-size: 1em;
    border-radius: 25px;
    margin-top: .3em;
    width: 100%;
    text-indent: 10px;
    outline: none;
    max-width: 350px;
    margin-bottom: 1em;
}

::placeholder {
    color: var(--gray);
    font-size: 1em;
    font-weight: 300;
}

#search_box:focus::placeholder {
  color: transparent;
}

.user {
    display: grid;
    grid-template-columns: 1fr 10fr 1fr;
    align-items: center;
    padding: .5em;
    cursor: pointer;
}

.user:hover {
    background-color: var(--itemBackground);
    transition: .2s;
}

.notification {
    display: flex;
    justify-content: center;
    background-color: var(--tweetBtnBg);
    border-radius: 35px;
}

.prifle_image {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    border: 1px solid white;
    margin-right: .6em;
}

.target_username, .target_name {
    display: inline;
}

.target_name { 
    font-weight: bold;
}

.target_username {
    color: var(--bordergray);
}

.middle_bottom > p {
    color: var(--bordergray);
    font-size: .8em;
}

.you, .message_preview {
    display: inline;
}

.you {
    padding-right: .3em;
    color: var(--bordergray);
}

.message_preview {
    font-weight: 100;
}
</style>