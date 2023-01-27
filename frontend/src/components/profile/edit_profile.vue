<template>
<div class="profile_modals_general">
    <div class="edit_profile_container">
        <div class="close_modal">
            <img id="clear_image_btn" src="@/assets/icons8-xbox-x-50.png" @click="this.$emit('toggle_modal_bool')">
        </div>
        <div class="profile_image_container">
            <img v-if="preview_image == null" :src="visited_user.profile_image">
            <img v-else :src="preview_image">
        </div>
        <div class="change_image_btn_container">
            <input type="file"
                    id="selected_file"
                    style="display: none;"
                    @change="validate_image_size"
                />
                <input id="add_image"
                    type="button"
                    value="Change Profile Image"
                    onclick="document.getElementById('selected_file').click();"
                />
        </div>
        <div class="name_container">
            <p class="label_text">Name</p>
            {{ character_limitor_name }}
            <input type="text" placeholder="Name" v-model="name">
        </div>
        <div class="bio_container">
            <p class="label_text">Biography</p>
            {{ character_limitor }}
            <textarea
                id="bio_textarea"
                placeholder="Bio"
                v-model="bio"
            ></textarea>
        </div>
        <div class="save_btn_container">
            <button id="save_btn" @click="edit_profile()">Save</button>
        </div>
    </div>
</div>
</template>

<script>
import {
    edit_profile_request
} from '@/requests'
export default {
    props: ["visited_user"],

    emits: ["toggle_modal_bool"],

    data() {
        return {
            bio: this.visited_user.biography,
            preview_image: null,
            name: this.visited_user.name,
        }
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
            const image = e.target.files[0];
            const reader = new FileReader();
            reader.readAsDataURL(image);
            reader.onload = e =>{
                //preview_image ll we saved database
                this.preview_image = e.target.result;
            };
        },

        async edit_profile() {
            let response_value = await edit_profile_request(this.preview_image, this.name, this.bio,)
            if(response_value) {
                this.$emit("toggle_modal_bool")
            }
        }
    },

    computed: {
        character_limitor() {
            if(this.bio.length > 160){
                this.bio = this.bio.substring(0, 160)
            }
        },

        character_limitor_name() {
            if(this.name.length > 25){
                this.name = this.name.substring(0, 25)
            }
        }
    }
}

</script>

<style scoped>
/*! EDIT PROFILE MODAL */
.edit_profile_container {
    background-color: var(--primaryBG);
    padding: 2em;
    border-radius: 50px;
}

.profile_image_container {
    display: flex;
    justify-content: center;
    margin-bottom: 1em;
}

.profile_image_container > img{
    width: 150px;
    height: 150px;
    border-radius: 50%;
    border: 1px solid white;
}

input {
    box-shadow: none;
    padding: .5em 1em .5em 1em;
    border: 1px solid var(--gray);
    margin-bottom: .5em;
    font-size: 1.1em;
    border-radius: 14px;
    background-color: var(--primaryBG);
}

input:focus {
    outline: 1px solid var(--tweetBtnBg);
}

textarea {
    border: none;
    font-weight: 300;
    font-size: 1.1em;
    padding: 0.2em;
    outline: none;
    width: 25em;
    height: 6em;
    resize: none;
    color: white;
    background-color: var(--primaryBG);
    border: 1px solid var(--bordergray);
    padding: .5em 1em .5em 1em;
    border-radius: 14px;
}

textarea:focus {
    outline: 1px solid var(--tweetBtnBg);
}

.label_text {
    margin-left: .3em;
    margin-bottom: .3em;
}

.save_btn_container {
    display: flex;
    justify-content: center;
    margin-top: 3em;
}

.change_image_btn_container {
    display: flex;
    justify-content: center;
    margin-bottom: 1em;
}

#add_image {
    color: var(--primaryBG);
    background-color: var(--colorWhite);
    padding: .5em;
    border-radius: 30px;
    font-weight: bold;
    margin-top: 1em;
    border-style: none;
}

#add_image:hover {
    transition: .1s;
    background-color: var(--whiteHover);
    color: black;
}

#save_btn {
    color: var(--colorWhite);
    background-color: var(--tweetBtnBg);
    font-size: 1.1em;
    padding: .5em 1em .5em 1em;
    border-radius: 30px;
    font-weight: bold;
    border-style: none;
}

#save_btn:hover {
    transition: .1s;
    background-color: var(--tweetBtnDarkBg);
}

.close_modal > img {
    width: 35px;
    filter: invert(99%) sepia(55%) saturate(453%) hue-rotate(256deg) brightness(122%) contrast(87%);
    cursor: pointer;
}
</style>