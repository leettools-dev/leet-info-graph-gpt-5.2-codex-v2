import { defineStore } from 'pinia'
import { fetchCurrentUser, loginWithGoogle, logout } from '../../../api/auth'

const TOKEN_KEY = 'infograph_token'
const USER_KEY = 'infograph_user'

const loadJson = (key) => {
  try {
    const value = localStorage.getItem(key)
    return value ? JSON.parse(value) : null
  } catch (error) {
    console.warn('Failed to parse persisted auth data', error)
    return null
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem(TOKEN_KEY) || '',
    user: loadJson(USER_KEY),
    status: 'idle',
    error: null,
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token),
  },
  actions: {
    setAuth({ token, user }) {
      this.token = token
      this.user = user
      this.error = null
      if (token) {
        localStorage.setItem(TOKEN_KEY, token)
      } else {
        localStorage.removeItem(TOKEN_KEY)
      }
      if (user) {
        localStorage.setItem(USER_KEY, JSON.stringify(user))
      } else {
        localStorage.removeItem(USER_KEY)
      }
    },
    async loginWithGoogleCredential(credential) {
      this.status = 'loading'
      this.error = null
      try {
        const { data } = await loginWithGoogle(credential)
        this.setAuth({ token: data.token, user: data.user })
        this.status = 'authenticated'
        return data.user
      } catch (error) {
        this.status = 'error'
        this.error = error
        throw error
      }
    },
    async hydrate() {
      if (!this.token) {
        return null
      }
      this.status = 'loading'
      try {
        const { data } = await fetchCurrentUser()
        this.user = data
        this.status = 'authenticated'
        return data
      } catch (error) {
        this.status = 'error'
        this.error = error
        this.setAuth({ token: '', user: null })
        return null
      }
    },
    async logout() {
      try {
        await logout()
      } catch (error) {
        console.warn('Logout request failed', error)
      } finally {
        this.setAuth({ token: '', user: null })
        this.status = 'idle'
      }
    },
  },
})
