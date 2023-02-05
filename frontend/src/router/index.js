import { createRouter, createWebHistory } from 'vue-router'

import signup from '@/views/registration/signup.vue'
import login from '@/views/registration/login.vue'
import forget_password from '@/views/registration/forget_password'

import main_layout from '@/views/main/main_layout.vue'
import home from '@/views/main/home.vue'
import tweet_page from '@/views/main/tweet_page.vue'
import topic_page from '@/views/main/topic_page.vue'
import explore from '@/views/main/explore.vue'
import profile from '@/views/main/profile.vue'
import messages from '@/views/main/messages.vue'
import message_page from '@/views/main/message_page.vue'

const routes = [
  {
    path: '/signup',
    name: 'signup',
    component: signup
  },

  {
    path: '/login',
    name: 'login',
    component: login
  },

  {
    path: '/forget_password',
    name: 'forget_password',
    component: forget_password
  },

  {
    path: '/main',
    name: 'main',
    component: main_layout,
    children: [
      {
        path: '/home',
        name: 'home',
        component: home
      },
      {
        path: '/tweet_page/:id',
        name: 'tweet_page',
        component: tweet_page
      },
      {
        path: '/topic/:string',
        name: 'topic',
        component: topic_page
      },
      {
        path: '/explore',
        name: 'explore',
        component: explore
      },
      {
        path: '/profile/:string/:profile_tab?',
        name: 'profile',
        component: profile
      },
      {
        path: '/messages',
        name: 'messages',
        componrnet: messages
      },
      {
        path: '/message_page/:target_username',
        name: 'message_page',
        component: message_page,
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
