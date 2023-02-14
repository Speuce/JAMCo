import { createRouter, createWebHistory } from 'vue-router'
import Sandbox from '@/views/Sandbox.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: () => import('../views/MainView.vue'),
    },
    {
      path: '/sandbox',
      name: 'sandbox',
      component: Sandbox,
    },
  ],
})

export default router
