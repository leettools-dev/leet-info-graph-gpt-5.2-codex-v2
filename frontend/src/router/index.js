import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../pages/auth/LoginPage.vue'
import ChatPage from '../pages/chat/ChatPage.vue'
import HistoryPage from '../pages/history/HistoryPage.vue'
import { useAuthStore } from '../stores/modules/auth'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'login', component: LoginPage },
  { path: '/chat', name: 'chat', component: ChatPage, meta: { requiresAuth: true } },
  { path: '/history', name: 'history', component: HistoryPage, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()
  if (authStore.token && !authStore.user) {
    await authStore.hydrate()
  }
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login' }
  }
  if (to.name === 'login' && authStore.isAuthenticated) {
    return { name: 'chat' }
  }
  return true
})

export default router
