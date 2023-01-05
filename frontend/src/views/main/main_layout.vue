<template>
<div class="main_layout_container">
    <div class="left">
        <div class="menu_container">
            <main_menu/>
        </div>
    </div>


    <div class="middle">
        <div class="header_container">
            <main_header
                :current_url="current_url"
            />
        </div>
        <div class="route_container">
            <home v-if="current_url == '/home'"></home>
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

import home from '@/views/main/home.vue'
    
export default {
    props: ["current_url"],

    components: {
        main_menu,
        main_trends,
        who_to_follow,
        searchbar,
        main_header,
        home,
    },
}
    
</script>
    
<style scoped>
.main_layout_container {
    display: flex;
    flex-direction: row;
    width: 1240px;
    gap: 1em;
}

.left {
    flex: .8;
}

.middle {
    flex: 2;
    border-left: 1px solid var(--bordergray);
    border-right: 1px solid var(--bordergray);
}

.right {
    flex: 1;
}

.header_container, .menu_container, .searchbar_container{
    position: -webkit-sticky;
    position: sticky;
    top: 0;    
}    
</style>