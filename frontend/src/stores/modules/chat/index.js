import { defineStore } from 'pinia'

import { createMessage, listMessages } from '../../../api/session'

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [],
    status: 'idle',
    error: null,
    isSending: false,
  }),
  getters: {
    hasMessages: (state) => state.messages.length > 0,
  },
  actions: {
    async fetchMessages(sessionId) {
      if (!sessionId) {
        this.messages = []
        return []
      }
      this.status = 'loading'
      this.error = null
      try {
        const { data } = await listMessages(sessionId)
        this.messages = data
        this.status = 'ready'
        return data
      } catch (error) {
        this.status = 'error'
        this.error = error
        throw error
      }
    },
    async sendMessage(sessionId, payload) {
      if (!sessionId) {
        throw new Error('Session id is required to send message')
      }
      this.isSending = true
      this.error = null
      try {
        const { data } = await createMessage(sessionId, payload)
        this.messages = [...this.messages, data]
        return data
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.isSending = false
      }
    },
    clearMessages() {
      this.messages = []
      this.status = 'idle'
      this.error = null
      this.isSending = false
    },
  },
})
