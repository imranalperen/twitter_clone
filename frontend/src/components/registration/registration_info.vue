<template>
<div class="registration_info_general_container">
    <div class="form_main">

        <div class="profile_picture">
            <div class="image_preview_container">
                <img v-if="preview_image == null" id="stok_image" class="image_preview" src="@/assets/depositphotos_137014128-stock-illustration-user-profile-icon.jpg">
                <img v-else :src="preview_image" class="image_preview"/>
            </div>
            <div class="file_select_container">
                <input type="file"
                    id="selected_file"
                    style="display: none;"
                    @change="validate_image_size"
                />
                <!-- input type file shows file name to ignore this we can do: -->
                <input id="add_image"
                    type="button"
                    value="Set Your Profile Image"
                    onclick="document.getElementById('selected_file').click();"
                />
            </div>
        </div>
        <div class="bio_container">
            {{ character_limitor }}
            <textarea
                id="bio_textarea"
                placeholder="Bio"
                v-model="bio"
            ></textarea>
        </div>

        <div class="buttons">
            <div class="accep_button_container">
                <button type="submit" id="next_btn" @click="next">Next</button>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import { registration_info_request } from '@/requests'

export default {
    
    data() {
        return {
            preview_image: null,
            error_message: '',
            bio: '',
            image_file: null,
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
            this.image_file = e.target.files[0]
            //preview
            const image = e.target.files[0]
            const reader = new FileReader()
            reader.readAsDataURL(image)
            reader.onload = e => {
                this.preview_image = e.target.result
            }
        },

        async next() {
            let response_value = await registration_info_request(this.image_file, this.bio)
            if(response_value) {
                this.push_main()
            }
        },

        push_main() {
            window.localStorage.removeItem("first_vizit")
            this.$router.push({name: "home"})
            location.reload()
        }
    },

    computed: {
        character_limitor() {
            if(this.bio.length > 160){
                this.bio = this.bio.substring(0, 160)
            }
        }
    }
}
</script>

<style scoped>
.registration_info_general_container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100%;
}

.form_main {
    padding: 2em;
    border: 1px solid var(--bordergray);
    border-radius: 35px;
}

.profile_picture {
    display: flex;
    flex-direction: column;
}

.image_preview_container, .file_select_container {
    display: flex;
    justify-content: center;
}

.image_preview_container > img {
    width: 150px;
    height: 150px;
    border-radius: 50%;
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

.buttons {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-top: 2em;
}


#next_btn {
    color: var(--colorWhite);
    background-color: var(--tweetBtnBg);
    font-size: 1.1em;
    padding: .5em 1em .5em 1em;
    border-radius: 30px;
    font-weight: bold;
    border-style: none;
}

#next_btn:hover {
    transition: .1s;
    background-color: var(--tweetBtnDarkBg);
}

.bio_container {
    margin-top: 1em;
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
</style>