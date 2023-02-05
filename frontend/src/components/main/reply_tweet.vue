<template>
    <div class="reply_tweet_container" id="reply_tweet_container_general">
        <div class="image_container" v-if="preview_image">
            <img :src="preview_image" class="image_preview"/>
            <img id="clear_image_btn" src="@/assets/icons8-xbox-x-50.png" @click="clear_preview_image">
        </div>
        <div class="reply_textarea_container">
            {{ character_limitor }}
            <textarea
                id="reply_textarea"
                placeholder="Tweet your reply..."
                v-model="tweet_text_body"
                @input="calculate_percent"
            ></textarea>
        </div>
        <div class="footer">
            <div class="footer_icon">
                <div class="reply_icon_container">
                    <input type="file"
                    id="reply_selected_file"
                    style="display: none;"
                    accept="image/png, image/jpeg"
                    @change="validate_image_size"
                />
                <img class="reply_icon" src="@/assets/image-outline.svg" onclick="document.getElementById('reply_selected_file').click();">
            </div>
        </div>
            <button id="tweet_reply_btn" @click="validate_tweet">Tweet</button>
        </div>
    </div>
</template>

<script>
import { add_replied_tweet_request } from "@/requests"

export default {
    props: ["toggle_reply_id"],

    emits: ["add_replied_tweet_timeline"],

    data() {
        return {
            tweet_text_body: "",
            preview_image: null,
            image_file: null,
        }
    },

    mounted() {
        document.getElementById("reply_tweet_container_general").addEventListener("keydown", function(e) {
            if(e.code == "Enter" && !e.shiftKey) {
                document.getElementById("tweet_reply_btn").click()
            }
        })
    },

    methods: {
        validate_image_size(e) {
            const file_size = e.target.files[0]
            if(file_size.size > 2097152) {
                console.log("File size shuld be less then 2 mb")
            }
            else{
                this.upload_image(e)
            }
        },


        upload_image(e){
            this.image_file = e.target.files[0]
            //preview
            const image = e.target.files[0];
            const reader = new FileReader();
            reader.readAsDataURL(image);
            reader.onload = e =>{
                this.preview_image = e.target.result;
            };
        },

        clear_preview_image() {
            return this.preview_image = null
        },

        validate_tweet() {
            if(this.preview_image) {
                if(this.tweet_text_body.length > 280) {
                    console.log("tweet length is too much")
                }
                else {
                    this.add_tweet()
                }
            }
            else {
                if(this.tweet_text_body.length < 1 || this.tweet_text_body.length > 280) {
                    console.log("no tweet or long tweet")
                }
                else {
                    this.add_tweet()
                }
            }
        },

        async add_tweet() {
            // const request_body = {
            //     "tweet_body": this.tweet_text_body,
            //     "tweet_image": this.preview_image,
            //     "tweet_id": this.toggle_reply_id
            // }
            // let response_value = await add_replied_tweet_request(request_body)
            let response_value = await add_replied_tweet_request(this.tweet_text_body, this.image_file, this.toggle_reply_id)
            if(response_value == 2001) {
                console.log("api tweeet length error")
            }
            else {
                this.tweet_text_body = ""
                this.preview_image = null
                this.$emit("add_replied_tweet_timeline")
            }
        },
    },

    computed: {
        character_limitor() {
            if(this.tweet_text_body.length > 280){
                this.tweet_text_body = this.tweet_text_body.substring(0, 280)
            }
        }
    }
}

</script>


<style scoped>
#reply_textarea {
    border: none;
    font-weight: 300;
    font-size: 1em;
    padding: 0.2em;
    outline: none;
    width: 100%;
    height: 4em;
    resize: none;
    color: white;
    background-color: var(--primaryBG);
}

.footer {
    display: flex;
    justify-content: space-between;
    padding-bottom: .3em;
}

#tweet_reply_btn {
    margin: .1em;
    color: var(--colorWhite);
    background-color: var(--tweetBtnBg);
    border-style: none;
    padding: .6em .8em;
    border-radius: 25px;
    font-weight: 500;
    font-size: .7em;
    cursor: pointer;
}

.reply_icon {
    width: 26px;
    filter: invert(45%) sepia(100%) saturate(662%) hue-rotate(173deg) brightness(94%) contrast(100%);
    margin-left: 1em;
    padding: 3px;
    border-radius: 50%;
}

.reply_icon:hover {
    transition: .1s;
    background: var(--itemBackground);
}

.image_container {
    position: relative;
}

.image_preview{
    margin-top: 1em;
    max-width: 550px;
    max-height: 550px;
    border-radius: 25px;
}

#clear_image_btn {
    filter: invert(99%) sepia(55%) saturate(453%) hue-rotate(256deg) brightness(122%) contrast(87%);
    width: 30px;
    position: absolute;
    top: 1.3em;
    left: .3em;
}
</style>