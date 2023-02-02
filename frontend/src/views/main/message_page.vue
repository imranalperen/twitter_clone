<style scoped>
.chat_page_general_container {
    display: flex;
    justify-content: space-between;
    flex-direction: column;
    height: 100vh;
    padding: .5em;
}

.chat_banner_container {
    position: -webkit-sticky;
    position: sticky;
    top: 0;
    background-color: rgba(21, 32, 43, .9);
    padding: 0 .2em .2em .2em;
}

.text_message_container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.message_text_container {
    padding-bottom: .5em;
    background-color: rgba(21, 32, 43, .9);
}

#message_input {
    background-color: var(--searchbarBG);
    border-style: none;
    padding: .7em;
    font-size: 1em;
    border-radius: 25px;
    margin-top: .3em;
    text-indent: 10px;
    outline: none;
    resize: none;
}

::placeholder {
    color: var(--itemBackground);
    font-size: 1em;
    font-weight: 300;
}

#message_input:focus::placeholder {
  color: transparent;
}

#sent_message_image {
    width: 29px;
    height: 28px;
    filter: invert(52%) sepia(53%) saturate(3711%) hue-rotate(179deg) brightness(99%) contrast(90%);
    cursor: pointer;
}

.main_user_message_container {
    display: flex;
    justify-content: end;
}

.target_user_message_container {
    display: flex;
}

.main_user_message_body {
    background-color: var(--tweetBtnBg);
}

.target_user_message_body {
    background-color: var(--itemBackground);
}
.main_user_message_body, .target_user_message_body {
    display: inline;
    padding: .7em;
    max-width: 80%;
    margin: .5em;
    border-radius: 15px;
}
</style>
<template>
<div class="chat_page_general_container">
    <div class="chat_container">
        <div class="chat_banner_container">
            <chat_banner/>
        </div>
        <div class="messages">
            <div class="message" v-for="message in chat_history" :key="message.id">
                <div class="main_user_message_container" v-if="message.sender_id == main_user.id">
                    <div class="main_user_message_body">
                        <p class="main_user_message_text">
                            {{ message.message }}
                        </p>
                    </div>
                </div>
                <div class="target_user_message_container" v-if="message.sender_id != main_user.id">
                    <div class="target_user_message_body">
                        <p class="target_user_message_text">
                            {{ message.message }}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="text_message_container">
        <div class="message_text_container">
            {{ character_limitor }}
            <textarea
                id="message_input"
                placeholder="Type your message..."
                v-model="message_body"
            ></textarea>
        </div>
        <div class="send_message_container">
            <img src="@/assets/icons8-sent-26.png" id="sent_message_image" @click="validate_message()">
        </div>
    </div>

</div>
</template>

<script>
import {
    chat_history_request,
    send_message_request
} from '@/requests'
import chat_banner from '@/components/main/chat_banner.vue'
export default {
    components: {
        chat_banner
    },

    props: ["main_user"],

    data() {
        return {
            message_body: '',
            target_username: null,
            chat_history: null,
        }
    },
    

    async beforeCreate() {
        this.target_username = this.$route.fullPath.split("/")[2]
        this.chat_history = await chat_history_request(this.target_username)
        this.chat_history = this.chat_history.response
    },

    methods: {
        validate_message() {
            this.send_message()
        },

        async send_message() {
            this.target_username = this.$route.fullPath.split("/")[2]
            let send_message_response = await send_message_request(this.target_username, this.message_body)
            console.log(send_message_response)
        }
    },

    computed: {
        character_limitor() {
            if(this.message_body.length > 500){
                this.message_body = this.message_body.substring(0, 500)
            }
        }
    },
}
</script>
