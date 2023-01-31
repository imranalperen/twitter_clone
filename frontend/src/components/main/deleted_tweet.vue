<template>
    <div class="deleted_tweet_container">
        <p class="deleted_tweet_text">This Tweet was deleted by the Tweet author.</p>
    </div>
</template>


<script>

</script>

<style scoped>
.deleted_tweet_container {
    background-color: rgb(32, 39, 49);
    display: flex;
    padding: .5em;
    border: 1px solid var(--bordergray);
    border-radius: 10px;
    justify-content: center;
    margin-bottom: .9em;
}

.deleted_tweet_text {
    color: var(--gray);
}
</style>