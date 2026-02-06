import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useAuthStore } from '../stores/modules/auth'

const GOOGLE_SCRIPT_ID = 'google-identity-service'

const loadGoogleScript = () =>
  new Promise((resolve, reject) => {
    if (document.getElementById(GOOGLE_SCRIPT_ID)) {
      resolve()
      return
    }
    const script = document.createElement('script')
    script.src = 'https://accounts.google.com/gsi/client'
    script.async = true
    script.defer = true
    script.id = GOOGLE_SCRIPT_ID
    script.onload = resolve
    script.onerror = () => reject(new Error('Failed to load Google Identity script'))
    document.head.appendChild(script)
  })

export const useGoogleAuth = () => {
  const authStore = useAuthStore()
  const isReady = ref(false)
  const error = ref(null)
  const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID

  const handleCredential = async (response) => {
    try {
      await authStore.loginWithGoogleCredential(response.credential)
    } catch (err) {
      error.value = err
    }
  }

  const initGoogle = async () => {
    if (!clientId) {
      error.value = new Error('Missing Google client ID')
      return
    }
    try {
      await loadGoogleScript()
      if (!window.google || !window.google.accounts || !window.google.accounts.id) {
        throw new Error('Google Identity Services unavailable')
      }
      window.google.accounts.id.initialize({
        client_id: clientId,
        callback: handleCredential,
      })
      isReady.value = true
    } catch (err) {
      error.value = err
    }
  }

  const renderButton = (element, options = {}) => {
    if (!isReady.value || !window.google?.accounts?.id) {
      return
    }
    window.google.accounts.id.renderButton(element, {
      theme: 'outline',
      size: 'large',
      width: 240,
      ...options,
    })
  }

  const prompt = () => {
    if (window.google?.accounts?.id) {
      window.google.accounts.id.prompt()
    }
  }

  onMounted(initGoogle)
  onBeforeUnmount(() => {
    if (window.google?.accounts?.id) {
      window.google.accounts.id.cancel()
    }
  })

  return {
    isReady,
    error,
    renderButton,
    prompt,
  }
}
