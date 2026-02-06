import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../pages/auth/LoginPage.vue'
import ChatPage from '../pages/chat/ChatPage.vue'
import HistoryPage from '../pages/history/HistoryPage.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'login', component: LoginPage },
  { path: '/chat', name: 'chat', component: ChatPage },
  { path: '/history', name: 'history', component: HistoryPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
