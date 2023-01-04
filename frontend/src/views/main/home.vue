<template>
<div class="home_container">
    <div class="tweet_container">
        <main_tweet/>
    </div>
    <div class="timeline">
        timeline
    </div> 
</div>
</template>

<script>
import main_tweet from '@/components/main/main_tweet.vue'

export default {
    components: {
        main_tweet
    },
}

</script>

<style scoped>


</style>