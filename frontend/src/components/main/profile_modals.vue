<style scoped>
.edit_profile_container {
    background-color: var(--primaryBG);
    padding: 7em;
    border-radius: 50px;
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

.profile_image_container {
    display: flex;
    justify-content: center;
    margin-bottom: 3em;
}

.profile_image_container > img{
    width: 150px;
    height: 150px;
    border-radius: 50%;
}

</style>

<template>
<div class="profile_modals_general" v-if="active_modal">
    <div class="edit_profile_container" v-if="active_modal == 'edit_profile'">
        <div class="profile_image_container">
            <img :src="user_infos.profile_image">
        </div>
        <div class="name_container">
            <p>Name</p>
            <input type="text" :value="user_infos.name">
        </div>
        <div class="bio_container">
            {{ character_limitor }}
            <textarea
                id="bio_textarea"
                placeholder="Bio"
                v-model="bio"
            ></textarea>
        </div>
    </div>

    <div class="follows_container" v-if="active_modal == 'follows'">
        follows acilacak
    </div>

    <div class="followers_container" v-if="active_modal == 'followers'">
        followers acilacak
    </div>

</div>
</template>

<script>
export default {
    props: ["active_modal", "user_infos"],

    data() {
        return {
            bio: ''
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

