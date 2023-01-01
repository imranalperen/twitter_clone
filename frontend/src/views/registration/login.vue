<template>
<div class="login_container">
    <div class="login_main">
        <div class="title">
            <img src="@/assets/icons8-twitter.svg">
            <p>Sign in to Clone</p>
        </div>
        <div class="user_form">
            <div class="form_element">
                <p>Username</p>
                <input type="text" placeholder="Username" v-model="username">
            </div>
            <div class="form_element">
                <p>Password</p>
                <input type="password" placeholder="*******" v-model="password">
            </div>
        </div>
        <p v-if="error_message" class="error">{{ error_message }}</p> 
        <button type="submit" id="login_btn" @click="login">Login</button>
        <button type="submit" id="signup_btn" @click="sign_up">Sign Up</button>
    </div>
</div>
</template>
    
    
<script>
import { login_request } from '@/requests'

export default {
    data() {
        return {
            username: '',
            password: '',
            error_message: '',
        }
    },

    beforeCreate() {
        if(window.localStorage["access_token"]){
            this.$router.push({name: "home"})
        }
    },

    methods: {

        async login() {
            if(this.username == '' || this.password == '') {
                this.error_message = "Please Fill All From"
            }
            else {
                let request_body = {
                    "username": this.username,
                    "password": this.password,
                }
                let response_value = await login_request(request_body)
                if(response_value.response == 1001) {
                    this.error_message = "No Such User Found"
                }
                else if(response_value.response == 1003) {
                    this.error_message = "Wrong Password"
                }
                else {
                    var access_token = response_value["access_token"]
                    window.localStorage.clear("access_token")
                    window.localStorage.setItem("access_token", access_token["token"])
                    this.$router.push({name: "home"})
                }
            }
        },

        sign_up() {
            this.$router.push({name: "signup"})
        }
    }

}
    
</script>
    
    
<style scoped>
.login_container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100%;
    background-color: var(--secondaryBG);
}

.login_main {
    background-color: var(--primaryBG);
    display: flex;
    flex-direction: column;
    padding: 3em 6em 4em 6em;
    border-radius: 5%;
}

.title {
    text-align: center;
    font-size: 1.7em;
    margin-bottom: 1em;
}

.title > img {
    width: 45px;
}

.user_form {
    display: flex;
    flex-direction: column;
}

.form_element > p {
    font-size: 1em;
    padding-bottom: .4em;
    padding-left: 1em;
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

#signup_btn{
    color: var(--primaryBG);
    background-color: var(--colorWhite);
    font-size: 1.3em;
    padding: .5em;
    border-radius: 30px;
    font-weight: bold;
    margin-top: 1em;
    border-style: none;
}

#signup_btn:hover {
    transition: .1s;
    background-color: var(--whiteHover);
    color: black;
}

#login_btn {
    color: var(--colorWhite);
    background-color: var(--tweetBtnBg);
    font-size: 1.3em;
    padding: .5em;
    border-radius: 30px;
    font-weight: bold;
    margin-top: 1em;
    border-style: none;
}

#login_btn:hover {
    transition: .1s;
    background-color: var(--tweetBtnDarkBg);
}

.error {
    font-style: italic;
    color: #ff3333;
    text-align: center;
    margin-top: .7em;
    font-size: .9em;
}
</style>