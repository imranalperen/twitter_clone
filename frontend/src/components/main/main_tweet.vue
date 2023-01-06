<template>
<div class="tweet_container">
    <div class="left">
        <div class="profile_image" v-if="user">
            <img :src="user.image">
        </div>
    </div>
    <div class="right">
        <div class="tweet_text_container">
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
                    <img class="icon" src="@/assets/image-outline.svg">
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
                    <button id="tweet_btn" @click="add_tweet">Tweet</button>
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

    data() {
        return {
            tweet_text_body: "",
            tweet_percent: 0,
            tweet_character_limit: 280,
        }
    },

    methods: {
        calculate_percent() {
            //character limit 280. all character input growth percent 100/280 percent
            let len = this.tweet_text_body.length
            this.tweet_percent = len*(100/280)
        },

        async add_tweet() {
            if(this.tweet_text_body.length < 1 || this.tweet_text_body > 280) {
                console.log("tweet uzun veya kisa")
            }
            else {
                let response_value = await add_tweet_request(this.tweet_text_body)
                if(response_value == 2001) {
                    console.log("api tweeet length error")
                }
                else {
                    this.tweet_text_body = ""
                    this.calculate_percent()
                }
            }
        }
    },
}

</script>

<style scoped>
.lv-textarea {
    background-color: red;
    color: blue;
}
.tweet_container {
    display: flex;
    border-bottom: 1px solid var(--bordergray);
}

.profile_image > img {
    width: 50px;
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
</style>