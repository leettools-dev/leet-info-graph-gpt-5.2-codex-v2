import { defineStore } from 'pinia'

import { createSession, deleteSession, getSession, listSessions } from '../../../api/session'

export const useSessionStore = defineStore('session', {
  state: () => ({
    sessions: [],
    activeSession: null,
    status: 'idle',
    error: null,
  }),
  actions: {
    async fetchSessions(params = { limit: 20, offset: 0 }) {
      this.status = 'loading'
      this.error = null
      try {
        const { data } = await listSessions(params)
        this.sessions = data
        this.status = 'ready'
        return data
      } catch (error) {
        this.status = 'error'
        this.error = error
        throw error
      }
    },
    async fetchSession(sessionId) {
      this.status = 'loading'
      this.error = null
      try {
        const { data } = await getSession(sessionId)
        this.activeSession = data
        this.status = 'ready'
        return data
      } catch (error) {
        this.status = 'error'
        this.error = error
        throw error
      }
    },
    async createSession(prompt) {
      this.status = 'loading'
      this.error = null
      try {
        const { data } = await createSession({ prompt })
        this.activeSession = data
        this.sessions = [data, ...this.sessions]
        this.status = 'ready'
        return data
      } catch (error) {
        this.status = 'error'
        this.error = error
        throw error
      }
    },
    async removeSession(sessionId) {
      this.status = 'loading'
      this.error = null
      try {
        await deleteSession(sessionId)
        this.sessions = this.sessions.filter((session) => session.session_id !== sessionId)
        if (this.activeSession && this.activeSession.session_id === sessionId) {
          this.activeSession = null
        }
        this.status = 'ready'
      } catch (error) {
        this.status = 'error'
        this.error = error
        throw error
      }
    },
    clearActiveSession() {
      this.activeSession = null
    },
  },
})
