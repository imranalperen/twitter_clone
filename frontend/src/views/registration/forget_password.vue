<template>
<div class="forget_password_general_container">
    <div class="forget_password_main">
        <div class="mail_adress_container">
            <label class="form_text">Mail Adress</label>
            <input type="text" v-model="mail_adress" id="mail_input" :disabled="step != 1">
            <div class="verify_btn_container">
                <button v-if="step == 1" class="verification_btn" @click="send_verification_code()">Send Verification Code</button>
            </div>
        </div>
        <div class="verify_code_container" v-if="step == 2">
            <label class="form_text">Verification Code</label>
            <input type="text" v-model="verify_code" placeholder="****">
            <label for="form_text">New Password</label>
            <input type="password" v-model="password" placeholder="********">
            <label for="form_text">Verify New Password</label>
            <input type="password" v-model="verify_password" placeholder="********">
            <button class="verification_btn" @click="validate_form()">Reset</button>
        </div>
        <div class="error_message_container" v-if="error">
            <p id="error_message">{{ error }}</p>
        </div>
        <div class="notice_message_container" v-if="notice">
            <p id="notice_message">{{ notice }}</p>
        </div>
    </div>
</div>
</template>

<script>
import {
    verification_code_request,
    reset_password_request
} from '@/requests'

export default {
    data() {
        return {
            mail_adress: null,
            error: null,
            mail_validation: null,
            notice: null,
            verify_code: '',
            step: 1,
            password: '',
            verify_password: ''
        }
    },

    methods: {
        async send_verification_code() {
            if(this.mail_adress) {
                this.validate_email()
                if(this.mail_validation) {
                    this.error = ""
                    let verify_code_response = await verification_code_request(this.mail_adress)
                    verify_code_response = verify_code_response.response
                    if(verify_code_response == 1002) {
                        this.error = "User can not found"
                    }
                    else if(verify_code_response == 9001) {
                        this.error = "An error occured. There is no more free email. Please try later."
                    }
                    else {
                        this.notice = `Verification code sended ${this.mail_adress}. Check your spams.`
                        this.step = 2
                    }
                }
                else {
                    this.error = "Invalid Mail Adress"
                }
            }
            else {
                this.error = "Please Fill The Maill Adress"
            }
        },

        validate_email() {
            if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(this.mail_adress)) {
                this.mail_validation = true
            } else {
                this.mail_validation = false
            }
        },

        async validate_form() {
            if(this.verify_code == '' || this.password == '' || this.verify_password == '') {
                this.error = "Please Fill The Form"
            }
            else if (this.password != this.verify_password) {
                this.password = ''
                this.verify_password = ''
                this.error = "Passwords Must Match"
            }
            else if(this.password.length > 10 || this.password.length < 5) {
                this.error = "Password Must Be 5-10 Characters."
            }
            else {
                let reset_password_respose = await reset_password_request(this.verify_code, this.password, this.mail_adress)
                reset_password_respose = reset_password_respose.response
                if(reset_password_respose == 1004) {
                    this.verify_code = ''
                    this.error = "Invalid Varification Code"
                }
                else {
                    this.$router.push({name: "login"})
                }
            }
        }

    },

}
</script>

<style scoped>
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

#mail_input {
    min-width: 300px;
}

.mail_adress_container {
    display: flex;
    flex-direction: column;
}

.forget_password_general_container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100%;
    background-color: var(--secondaryBG);

}
.verify_btn_container {
    display: flex;
    justify-content: center;
}
.forget_password_main {
    padding: 3em 6em 4em 6em;
    background-color: var(--primaryBG);
    border-radius: 25px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.verification_btn{
    color: var(--primaryBG);
    background-color: var(--colorWhite);
    padding: .5em;
    border-radius: 30px;
    font-weight: bold;
    border-style: none;
}

.verification_btn:hover {
    transition: .1s;
    background-color: var(--whiteHover);
    color: black;
}

#error_message {
    font-style: italic;
    color: #ff3333;
    text-align: center;
    margin-top: .7em;
    font-size: .9em;
}

#notice_message {
    font-size: .8em;
    text-align: center;
    margin-top: .7em;
    max-width: 300px;
    color: var(--tweetBtnBg);
}

.verify_code_container {
    display: flex;
    flex-direction: column;
    margin-top: .8em;
}
</style>