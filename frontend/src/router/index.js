import { createRouter, createWebHistory } from 'vue-router'
import signup from '@/views/registration/signup.vue'
import login from '@/views/registration/login.vue'
import home from '@/views/main/home.vue'
import main_layout from '@/views/main/main_layout.vue'

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
    path: '/main',
    name: 'main',
    component: main_layout,
    children: [
      {
        path: '/home',
        name: 'home',
        component: home
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
