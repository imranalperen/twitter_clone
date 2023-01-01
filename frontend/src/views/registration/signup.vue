<template>
<div class="signup_container">
    <div class="signup_main">
        <div class="title">
            <img src="@/assets/icons8-twitter.svg">
            <p>Join Clone Today</p>
        </div>
        <div class="user_form">
            <div class="form_element">
                <p>Name</p>
                <input type="text" placeholder="Name" v-model="name">
            </div>
            <div class="form_element">
                <p>Username</p>
                <input type="text" placeholder="Username" v-model="username">
            </div>
            <div class="form_element">
                <p>Email</p>
                <input type="email" placeholder="example@mail.com" v-model="email">
            </div>
            <div class="form_element">
                <p>Password</p>
                <input type="password" placeholder="*******" v-model="password">
            </div>
            <div class="form_element">
                <p>Verify Password</p>
                <input type="password" placeholder="*******" v-model="verify_password">
            </div>
        </div>
        <p v-if="error_message" class="error">{{ error_message }}</p> 
        <button type="submit" id="signup_btn" @click="validate_form">Sign Up</button>
        <button type="submit" id="login_btn" @click="login">Login</button>
    </div>
</div>
</template>


<script>
import { signup_request } from '@/requests';

export default {
    data() {
        return{
            name: '',
            username: '',
            email: '',
            password: '',
            verify_password: '',
            error_message: ''
        }
    },

    methods: {
        validate_form() {
            if( this.name == '' || this.username == '' || this.email == '' || this.password == '' || this.verify_password == '') {
                this.error_message = "Please Fill All Form."
            }
            else if (this.username.length > 15 || this.username.length < 5) {
                this.error_message = "Username Must Be 5-15 Characters."
            }
            else if(this.username.includes(" ")) {
                this.error_message = "Username Doesn't Have Space."
            }
            else if(this.password.length > 10 || this.password.length < 5) {
                this.error_message = "Password Must Be 5-10 Characters."
            }
            else if(this.email.length > 30) {
                this.error_message = "Email Must Be Less Then 30 Character.s"
            }
            else if (this.name.length > 25) {
                this.error_message = "Username Must Be Less Then 25 Characters."
            }
            else if(this.password != this.verify_password) {
                this.password = null
                this.verify_password = null
                this.error_message = "Passwords Must Match."
            }
            else {
                this.validate_email(this.email)
            }
        },

        validate_email(mail_adress) {
            if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail_adress)) {
                this.send_from()
            } else {
                this.email = null
                this.error_message = "Invalid Email Adress"
            }
        },

        async send_from() {
            let request_body = {
                "name": this.name,
                "username": this.username,
                "email": this.email,
                "password": this.password,
                }
            
            let response_value = await signup_request(request_body)
            if(response_value.response == 1001) {
                this.error_message = "Username already registered."
            }
            else if (response_value.response == 1002) {
                this.error_message = "Email already registered."
            }
            else {
                this.login()
            }
        },

        login() {
            this.$router.push({name: "login"})
        }
    },
}
</script>


<style scoped>
.signup_container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100%;
    background-color: var(--secondaryBG);
}

.signup_main {
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
    transition: .2s;
    /* background-color: var(--gray); */
    background-color: #b5b5b5;
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