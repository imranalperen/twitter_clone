<template>
    <div class="chat_banner_container" v-if="target_username && target_profile_image" @click="redirct_user_page()">
        <div class="user_profile_image">
            <img :src="target_profile_image" class="profile_image">
        </div>
        <h1 class="selectable_title">{{ target_username }}</h1>
    </div>
</template>

<script>
import { user_profile_image_request } from '@/requests'
export default {
    data() {
        return {
            target_username: null,
            target_profile_image: null
        }
    },

    async beforeCreate() {
        this.target_username = this.$route.fullPath.split("/")[2]
        this.target_profile_image = await user_profile_image_request(this.target_username)
        this.target_profile_image = this.target_profile_image.response
        this.target_username = this.$route.fullPath.split("/")[2]
    },

    methods: {

        redirct_user_page() {
            this.$router.push({name: 'profile', params: {string: `${this.target_username}`, profile_tab: null}})
        }
    }
}
</script>

<style scoped>

.selectable_title {
    font-size: 1em;
    font-weight: 400;
    cursor: pointer;
}

.selectable_title:hover {
    text-decoration: underline;
}

.profile_image {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 1px solid white;
}

.chat_banner_container {
    display: flex;
    align-items: center;
    gap: .5em;
}
</style>