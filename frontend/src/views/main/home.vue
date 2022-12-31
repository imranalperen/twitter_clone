<template>
<div class="home_container">

    <div class="left">
        <div class="menu_container">
            <main_menu/>
        </div>
    </div>


    <div class="middle">
        <div class="header_container">
            <main_header/>
        </div>
        <div class="tweet_container">
            <main_tweet/>
        </div>
        <div class="timeline">
            timeline
        </div> 
    </div>


    <div class="right">
        <div class="searchbar_container">
            <searchbar/>
        </div>
        <div class="trends_container">
            <main_trends/>
        </div>
        <div class="who_to_follow_container">
            <who_to_follow/>
        </div>
    </div>

</div>
</template>

<script>
import main_menu from '@/components/main/main_menu.vue';
import main_trends from '@/components/main/main_trends.vue';
import who_to_follow from '@/components/main/who_to_follow.vue';
import searchbar from '@/components/main/searchbar.vue'
import main_header from '@/components/main/main_header.vue'
import main_tweet from '@/components/main/main_tweet.vue'

export default {
    components: {
        main_menu,
        main_trends,
        who_to_follow,
        searchbar,
        main_header,
        main_tweet
    },

    data() {
        return {
            user: [],
        }
    },

    async beforeCreate() {
        
    }
}

</script>

<style scoped>
.home_container {
    display: flex;
    width: 1240px;
}

.left{
    flex: .8;
}

.menu_container {
    position: -webkit-sticky; /* Safari */
    position: sticky;
    top: 0;
}

.middle {
    flex: 2;
    margin-right: 1.5em;
    border-left: 1px solid var(--bordergray);
    border-right: 1px solid var(--bordergray);
}

.right {
    flex: 1;
}

.searchbar_container {
    position: -webkit-sticky; /* Safari */
    position: sticky;
    top: 0;
}


</style>