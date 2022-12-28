import { createRouter, createWebHistory } from 'vue-router'
import signup from '@/views/registration/signup.vue'
import login from '@/views/registration/login.vue'
import home from '@/views/main/home.vue'

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
    path: '/home',
    name: 'home',
    component: home
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
