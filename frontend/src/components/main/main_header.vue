<template>
<div class="header_main">
    <div class="header_title">
        <h1 v-if="current_url == '/home'">Home</h1>
    </div>
</div>
</template>

<script>
export default {
    props: ["current_url"]
}
</script>

<style scoped>
.header_title {
    padding: .5em 0 1.2em 1em;
    background-color: rgba(21, 32, 43, .9);
}

h1 {
    font-size: 1.3em;
    font-weight: 400;
}

</style>