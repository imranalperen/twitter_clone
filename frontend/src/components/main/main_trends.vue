<template>
<div class="main_trends">
    <div class="title">
        <h1>Trends</h1>
    </div>
    <div class="trends">
        <div class="trend">
            <p class="trend_title">#trend1</p>
            <p class="trend_tweet">1,723 Tweets</p>
        </div>
        <div class="trend">
            <p class="trend_title">#trend2</p>
            <p class="trend_tweet">7,721 Tweets</p>
        </div>
        <div class="trend">
            <p class="trend_title">#trend3</p>
            <p class="trend_tweet">6,618 Tweets</p>
        </div>
        <div class="trend">
            <p class="trend_title">#trend4</p>
            <p class="trend_tweet">99,124 Tweets</p>
        </div>
        <div class="trend">
            <p class="trend_title">#trend5</p>
            <p class="trend_tweet">3,512 Tweets</p>
        </div>
    </div>
</div>
</template>

<script>
export default {

}
</script>

<style scoped>
.main_trends {
    background-color: var(--thirdBG);
    margin-top: .5em;
    padding: 1em 0 1.4em 0;
    border-radius: 25px;
}

h1 {
    font-size: 1.4em;
    padding-left: .6em;
}

.trend {
    padding: .5em 0 .5em 0;
    cursor: pointer;
    padding-left: 1em;
}

.trend_title {
    font-weight: 500;
}

.trend_tweet {
    font-size: .85em;
    color: var(--gray);
    margin-top: .1em;
}

.trend:hover {
    background-color: var(--itemBackground);
    transition: .3s;
}

</style>