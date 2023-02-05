<template>
<div class="main_layout_container" v-if="first_vizit">
    <registration_info/>
</div>

<div class="main_layout_container" v-else>
    <div class="left">
        <div class="menu_container">
            <main_menu
                :user="user"
            />
        </div>
    </div>


    <div class="middle">
        <div class="header_container">
            <main_header
                :current_url="current_url"
            />
        </div>
        <div class="route_container">
            <home
                v-if="current_url == 'home'"
                :user="user"
            ></home>
            <tweet_page
                v-if="current_url == 'tweet_page'"
                :user="user"
            ></tweet_page>
            <topic_page
                v-if="current_url == 'topic'"
                :user = user
            ></topic_page>
            <explore
                v-if="current_url == 'explore'"
                :user = user
            ></explore>
            <profile
                v-if="current_url == 'profile'"
                :user = user
            ></profile>
            <messages
                v-if="current_url == 'messages'"
                :main_user = user
            ></messages>
            <message_page
                v-if="current_url == 'message_page'"
                :main_user = user
            ></message_page>
            <notifications
                v-if="current_url == 'notifications'"
                :user = user
            ></notifications>
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
            <who_to_follow
                :user="user"
            />
        </div>
    </div>

</div>
</template>
    
<script>
import registration_info from '@/components/registration/registration_info.vue'
import main_menu from '@/components/main/main_menu.vue'
import main_trends from '@/components/main/main_trends.vue'
import who_to_follow from '@/components/main/who_to_follow.vue'
import searchbar from '@/components/main/searchbar.vue'
import main_header from '@/components/main/main_header.vue'

import home from '@/views/main/home.vue'
import tweet_page from '@/views/main/tweet_page.vue'
import topic_page from '@/views/main/topic_page.vue'
import explore from '@/views/main/explore.vue'
import profile from '@/views/main/profile.vue'
import messages from '@/views/main/messages.vue'
import message_page from '@/views/main/message_page.vue'
import notifications from '@/views/main/notifications.vue'

import { user_request } from '@/requests'
    
export default {
    props: ["current_url"],

    components: {
        registration_info,
        main_menu,
        main_trends,
        who_to_follow,
        searchbar,
        main_header,
        home,
        tweet_page,
        topic_page,
        explore,
        profile,
        messages,
        message_page,
        notifications
    },

    data() {
        return {
            first_vizit: null,
            user: null,
        }
    },

    async beforeCreate() {
        if(window.localStorage.getItem("first_vizit")) {
            this.first_vizit = await true
        }
        this.user = await user_request()
        this.user = this.user.response[0]
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

.header_container {
    z-index: 9;
}

</style>