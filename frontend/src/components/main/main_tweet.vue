<template>
<div class="tweet_container" id="tweet_container_general">
    <div class="left">
        <div class="profile_image" v-if="user">
            <img :src="user.profile_image">
        </div>
    </div>
    <div class="right">
        <div class="tweet_text_container">
            <div class="image_container" v-if="preview_image">
                <img :src="preview_image" class="image_preview"/>
                <img id="clear_image_btn" src="@/assets/icons8-xbox-x-50.png" @click="clear_preview_image">
            </div>
            {{ character_limitor }}
            <textarea
                id="tweet_textarea"
                placeholder="What's happening?"
                v-model="tweet_text_body"
                @input="calculate_percent"
            ></textarea>
        </div>
        <div class="tweet_footer">
            <div class="footer_left">
                <div class="icon_container">
                    <input type="file"
                    id="selected_file"
                    accept="image/png, image/jpeg"
                    style="display: none;"
                    @change="validate_image_size"
                />
                <!-- input type file shows file name to ignore this we can do: -->
                <img class="icon" src="@/assets/image-outline.svg" onclick="document.getElementById('selected_file').click();">
                </div>
            </div>
            <div class="footer_right">
                <div class="tweet_btn_container">
                    <div class="progress_container">
                        <circle-progress
                            :percent="tweet_percent"
                            :size="20"
                            :border-bg-width="3"
                            :border-width="3"
                        />
                    </div>
                    <button id="tweet_btn" @click="validate_tweet">Tweet</button>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import "vue3-circle-progress/dist/circle-progress.css"
import CircleProgress from "vue3-circle-progress"

import { add_tweet_request } from "@/requests"

export default {
    components: {
        CircleProgress
    },

    props: ["user"],

    emits: ["refresh_tweets"],

    data() {
        return {
            tweet_text_body: "",
            tweet_text_body_trash: "",
            tweet_percent: 0,
            tweet_character_limit: 280,
            preview_image: null,
            image_file: null,
        }
    },

    mounted() {
        document.getElementById("tweet_container_general").addEventListener("keydown", function(e) {
            if(e.code == "Enter" && !e.shiftKey) {
                document.getElementById("tweet_btn").click()
            }
        })
    },

    methods: {
        calculate_percent() {
            //character limit 280. all character input growth percent 100/280 percent
            let len = this.tweet_text_body.length
            this.tweet_percent = len*(100/280)
        },

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
                //preview_image ll we saved database
                this.preview_image = e.target.result;
            };
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
            let response_value = await add_tweet_request(this.tweet_text_body, this.image_file)
            if(response_value == 2001) {
                console.log("api tweeet length error")
            }
            else {
                this.tweet_text_body = ""
                this.preview_image = null
                this.calculate_percent()
                this.$emit("refresh_tweets")
            }
        },

        clear_preview_image() {
            return this.preview_image = null
        }
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
.tweet_container {
    display: flex;
    border-bottom: 1px solid var(--bordergray);
}

.profile_image > img {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin: .8em;
}
.left {
    flex: 1;
}

.right {
    display: flex;
    flex-direction: column;
    flex: 10;
}

#tweet_textarea{
    border: none;
    font-weight: 300;
    font-size: 1.1em;
    padding: 0.2em;
    outline: none;
    width: 100%;
    height: 6em;
    resize: none;
    color: white;
    background-color: var(--primaryBG);
}

.tweet_footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: .3em;
}

.icon {
    width: 26px;
    filter: invert(45%) sepia(100%) saturate(662%) hue-rotate(173deg) brightness(94%) contrast(100%);
    margin-left: 1em;
    padding: 3px;
    border-radius: 50%;
    cursor: pointer;
}

.icon:hover {
    transition: .1s;
    background: var(--itemBackground);
}

.tweet_btn_container {
    display: flex;
    margin-right: .5em;
}

#tweet_btn {
    margin: .1em;
    color: var(--colorWhite);
    background-color: var(--tweetBtnBg);
    border-style: none;
    padding: .8em 1em;
    width: 100%;
    border-radius: 25px;
    font-weight: 500;
    font-size: .9em;
    cursor: pointer;
}

#tweet_btn:hover {
    background-color: var(--tweetBtnDarkBg);
}

.progress_container{
    display: flex;
    align-items: center;
    margin-right: 1em;
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