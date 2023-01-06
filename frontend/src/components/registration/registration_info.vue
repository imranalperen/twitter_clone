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
                    @change="validagte_image_size"
                />
                <!-- input type file shows file name to ignore this we can do: -->
                <input id="add_image"
                    type="button"
                    value="Set Your Profile Image"
                    onclick="document.getElementById('selected_file').click();"
                />
            </div>
        </div>

        <div class="date_of_birth_container">
            <p class="birth_text">Date Of Birth</p>
            <div class="date_pick">
                <Datepicker
                    v-model="date"
                    :dark=true
                    position="center"
                    :enable-time-picker="false"
                ></Datepicker>
            </div>
        </div>
        <div class="gender">
            <div class="gender_container">
                <p>Gender</p>
                <input type="radio" id="male" name="gender_radio" value="male" checked>
                <label for="male">Male</label><br>
                <input type="radio" id="female" name="gender_radio" value="female">
                <label for="female">Female</label><br>
            </div>
        </div>
        <div class="informations">
            <div class="info_container">
                <p class="info">You can verify your email from your profile and get a free blue tick.</p>
            </div>
            <div class="error_container" v-if="error_message">
                <p class="error">{{error_message}}</p>
            </div>
        </div>
        <div class="buttons">
            <div class="skip_button_container">
                <button type="submit" id="skip_btn" @click="skip">Skip</button>
            </div>
            <div class="accep_button_container">
                <button type="submit" id="next_btn" @click="next">Next</button>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import Datepicker from '@vuepic/vue-datepicker';
import { registration_info_request } from '@/requests'

export default {
    components: { Datepicker },
    
    data() {
        return {
            preview_image: null,
            date: null,
            gender_options: [{"name": "Male"}, {"name": "Female"}],
            error_message: ""
        }
    },

    methods: {
        validagte_image_size(e) {
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

        async skip() {
            //set defaul image from local
            const stok_image = document.getElementById("stok_image").src
            const request_body = {
                "profile_image": stok_image
            }
            let response_value = await registration_info_request(request_body)
            if(response_value) {
                    this.push_main()
            }
        },

        async next() {
            let gender = document.querySelector('input[name="gender_radio"]:checked').value;
            if(this.preview_image == null || this.date == null ) {
                this.error_message = "Please Fill All The Form"
            }
            else{
                const request_body = {
                    "profile_image": this.preview_image,
                    "date_of_birth": this.date,
                    "gender": gender
                }
                let response_value = await registration_info_request(request_body)
                if(response_value) {
                    this.push_main()
                }
            }
        },        

        push_main() {
            window.localStorage.removeItem("first_vizit")
            this.$router.push({name: "home"})
            location.reload()
        }
    },
}
</script>

<style scoped>
.dp__theme_dark {
   --dp-background-color: #212121;
   --dp-text-color: #ffffff;
   --dp-hover-color: #484848;
   --dp-hover-text-color: #ffffff;
   --dp-hover-icon-color: #959595;
   --dp-primary-color: #005cb2;
   --dp-primary-text-color: #ffffff;
   --dp-secondary-color: #a9a9a9;
   --dp-border-color: var(--bordergray);
   --dp-menu-border-color: #2d2d2d;
   --dp-border-color-hover: #aaaeb7;
   --dp-disabled-color: #737373;
   --dp-scroll-bar-background: #212121;
   --dp-scroll-bar-color: #484848;
   --dp-success-color: var(--tweetBtnBg);
   --dp-success-color-disabled: var(--tweetBtnBg);
   --dp-icon-color: #959595;
   --dp-danger-color: #e53935;
   --dp-highlight-color: rgba(0, 92, 178, 0.2);
}

.registration_info_general_container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100%;
}

.form_main {
    padding: 1em 1em 1em 1em;
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

.date_of_birth_container {
    padding-top: 2em;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.birth_text {
    font-size: .9em;
    text-align: center;
    margin-bottom: .4em;
}

.date_pick {
    padding: 0 2em 0 2em;
}

.gender {
    padding-top: 2em;
    display: flex;
    justify-content: center;
}

.gender_container > p {
    padding-bottom: .5em;
}

.gender_container > label {
    padding-left: .4em;
}

.informations {
    padding-top: 2em;
    font-style: italic;
    font-weight: 100;
    display: flex;
    flex-direction: column;
    justify-content: center;
    font-size: .8em;
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

#skip_btn {
    color: var(--primaryBG);
    background-color: var(--colorWhite);
    font-size: 1.1em;
    padding: .5em;
    border-radius: 30px;
    font-weight: bold;
    border-style: none;
}

#skip_btn:hover {
    transition: .1s;
    background-color: var(--whiteHover);
    color: black;
}

.error {
    color: red;
    text-align: center;
    margin-top: 1em;
}
</style>