import { computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/modules/auth'

export const useAuth = () => {
  const authStore = useAuthStore()

  const user = computed(() => authStore.user)
  const token = computed(() => authStore.token)
  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const status = computed(() => authStore.status)

  onMounted(() => {
    authStore.hydrate()
  })

  return {
    authStore,
    user,
    token,
    isAuthenticated,
    status,
  }
}
