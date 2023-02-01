<template>
<div class="chat_page_general_container">
    <div class="chat_container">
        burasi chat container
        
    </div>
    <div class="message_text_container">
        burasi text input containeri
    </div>
</div>
</template>

<script>
import {  } from '@/requests'
export default {
    props: ["main_user"],

    data() {
        return {
            target_user: null,
        }
    },
    

    async beforeCreate() {
        let target_username = this.$route.fullPath.split("/")[2]
        
    }
}
</script>

<style scoped>

</style>