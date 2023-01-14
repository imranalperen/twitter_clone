<template>
<div class="header_main">
    {{ calculate_goback }}
    <div class="go_back" v-if="goback">
        <img src="@/assets/icons8-left-arrow-60.png" @click="go_previus_page">
    </div>
    <div class="header_title">
        <h1 v-if="current_url == 'home'">Home</h1>
    </div>
</div>
</template>

<script>
export default {
    props: ["current_url"],

    data() {
        return {
            goback: false
        }
    },

    methods: {
        go_previus_page() {
            this.$router.go(-1)
        }
    },

    computed: {
        calculate_goback() {
            if(this.current_url == 'tweet_page') {
                this.goback = true
            }
            else {
                this.goback = false
            }
        }
    }
}
</script>

<style scoped>
.header_main {
    display: flex;
}

.go_back > img {
    filter: invert(100%) sepia(9%) saturate(13%) hue-rotate(247deg) brightness(112%) contrast(87%);
    width: 25px;
    margin-top: .6em;
    margin-left: .3em;
    cursor: pointer;
}
.header_title {
    padding: .5em 0 1.2em 1em;
    background-color: rgba(21, 32, 43, .9);
}

h1 {
    font-size: 1.3em;
    font-weight: 400;
}

</style>