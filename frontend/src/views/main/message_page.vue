<template>
<div class="chat_page_general_container">
    <div class="chat_container">
        <div class="chat_banner_container">
            <chat_banner/>
        </div>
        <div id="messages" v-if="main_user">
            <div class="message" v-for="message in chat_history">
                <div class="main_user_message_container" v-if="message.sender_id == main_user.id">
                    <div class="main_user_message_body">
                        <p class="main_user_message_text">
                            {{ message.message }}
                        </p>
                    </div>
                </div>
                <div class="target_user_message_container" v-if="message.sender_id != main_user.id">
                    <div class="target_user_message_body" v-if="message.message">
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
    send_message_request,
    get_chat_id_request,
    mark_as_read_message_request
} from '@/requests'
import chat_banner from '@/components/main/chat_banner.vue'
import { ABLY_API_KEY } from '@/localsettings'
import Ably from 'ably'
export default {
    components: {
        chat_banner
    },

    props: ["main_user"],

    data() {
        return {
            message_body: '',
            message_body_temp: null,
            target_username: null,
            chat_history: null,
            chat_id: null,
            ably_channel: null
        }
    },
    

    async beforeCreate() {
        this.target_username = this.$route.fullPath.split("/")[2]
        this.chat_history = await chat_history_request(this.target_username)
        this.chat_history = this.chat_history.response

        this.target_username = this.$route.fullPath.split("/")[2]
        this.chat_id = await get_chat_id_request(this.target_username)
        this.chat_id = this.chat_id.response

        mark_as_read_message_request(this.chat_id)

        const ably = new Ably.Realtime.Promise(`${ABLY_API_KEY}`)
        this.ably_channel = ably.channels.get(`${this.chat_id}`)
        await ably.connection.once('connected');
        await this.ably_channel.subscribe(`${this.chat_id}`, (message) => {
            //last message add as first element of chat history
            const msg_data = message.data
            const msg = {
                "chat_id": msg_data.chat_id,
                "date": msg_data.date,
                "message": msg_data.message,
                "sender_id": msg_data.sender_id,
            }
            this.chat_history = [msg].concat(this.chat_history)
        });
    },

    mounted() {
        document.getElementById("message_input").addEventListener("keydown", function(e) {
            if(e.code == "Enter" && !e.shiftKey) {
                e.preventDefault()
                document.getElementById("sent_message_image").click()
            }
        })
    },

    async beforeUnmount() {
        mark_as_read_message_request(this.chat_id)
    },

    methods: {
        validate_message() {
            this.message_body_temp = this.message_body
            this.message_body = ''
            if(this.message_body_temp.length > 1) {
                this.send_message()
            }
        },

        async send_message() {
            this.target_username = this.$route.fullPath.split("/")[2]
            await send_message_request(this.target_username, this.message_body_temp)
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

<style scoped>
.chat_page_general_container {
    display: flex;
    justify-content: space-between;
    flex-direction: column;

    /* height: 100vh; */
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
    display: flex;
    flex-direction: column;
    flex: 1;
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
    margin-left: .5em;
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

.icon {
    width: 45px;
    filter: invert(45%) sepia(100%) saturate(662%) hue-rotate(173deg) brightness(94%) contrast(100%);
    padding: .5em;
    margin: 0 .5em 0 .5em;
    cursor: pointer;
    border-radius: 50%;
}

.icon:hover {
    transition: .1s;
    background: var(--itemBackground);
}
#messages {
    overflow: scroll;
    overflow-x: hidden;
    display: flex;
    flex-direction: column-reverse;
    height: 82vh;
}

.chat_container {
    height: 90vh;
    /* development */
}

/* width */
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
</style>