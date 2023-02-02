<template>
<div class="chat_page_general_container">
    <div class="chat_container">
        <div class="chat_banner_container">
            <chat_banner/>
        </div>
        <div class="messages">
            messages burada olacak nasilina bakicaz
        </div>
    </div>
    <div class="text_message_container">
        <div class="message_text_container">
            {{ character_limitor }}
            <textarea
                id="message_input"
                placeholder="Type your message..."
                v-model="message_text"
            ></textarea>
        </div>
        <div class="send_message_container">
            <img src="@/assets/icons8-sent-26.png" id="sent_message_image">
        </div>
    </div>

</div>
</template>

<script>
import { chat_history_request } from '@/requests'
import chat_banner from '@/components/main/chat_banner.vue'
export default {
    components: {
        chat_banner
    },

    data() {
        return {
            message_text: '',
        }
    },
    

    async beforeCreate() {
        let target_username = this.$route.fullPath.split("/")[2]
        let chat_history = await chat_history_request(target_username)
        console.log(chat_history.response)
    },

    methods: {

    },

    computed: {
        character_limitor() {
            if(this.message_text.length > 500){
                this.message_text = this.message_text.substring(0, 500)
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
    width: 102vh;
    resize: none;
}

::placeholder {
    color: var(--gray);
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
</style>