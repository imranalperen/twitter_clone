<template>
<div class="notifications_general_container">
    <div class="notification_bar">
        <div class="profile_image">profil fotosu</div>
        <div class="notification_text">someone like your tweet.</div>
    </div>
    <div class="notification_bar">
        <div class="profile_image">profil fotosu</div>
        <div class="notification_text">someone retweet your tweet.</div>
    </div>
    <div class="notification_bar">
        <div class="profile_image">profil fotosu</div>
        <div class="notification_text">someone replied your tweet.</div>
    </div>
</div>
</template>

<script>
export default {
    props: ["user"],

    data() {
        return {

        }
    },

    beforeCreate() {
        
    }
}

</script>

<style scoped>
.notifications_general_container {
    display: flex;
    flex-direction: column;
}
.notification_bar {
    display: flex;
    flex-direction: column;
    padding: .5em;
    border-top: 1px solid var(--bordergray);
}
</style>