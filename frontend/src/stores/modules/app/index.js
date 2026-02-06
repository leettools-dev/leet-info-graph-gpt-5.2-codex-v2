import { defineStore } from 'pinia'
import { fetchHealth } from '../../../api/health'

export const useAppStore = defineStore('app', {
  state: () => ({
    backendHealthy: false,
    backendStatus: 'unknown',
  }),
  actions: {
    async checkBackend() {
      try {
        await fetchHealth()
        this.backendHealthy = true
        this.backendStatus = 'connected'
      } catch (error) {
        this.backendHealthy = false
        this.backendStatus = 'unavailable'
        console.error('Health check failed', error)
      }
    },
  },
})
