import request from '../utils/request'

export const createSession = (payload) => request.post('/api/v1/sessions', payload)

export const listSessions = (params = {}) =>
  request.get('/api/v1/sessions', {
    params,
  })

export const getSession = (sessionId) => request.get(`/api/v1/sessions/${sessionId}`)

export const deleteSession = (sessionId) => request.delete(`/api/v1/sessions/${sessionId}`)
