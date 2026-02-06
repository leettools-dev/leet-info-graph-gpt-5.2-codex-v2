import axios from 'axios'
import { pinia } from '../stores'
import { useAuthStore } from '../stores/modules/auth'

const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const request = axios.create({
  baseURL: apiBase,
  timeout: 10000,
})

request.interceptors.request.use((config) => {
  const authStore = useAuthStore(pinia)
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
})

export default request
