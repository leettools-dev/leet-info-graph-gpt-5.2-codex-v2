import request from '../utils/request'

export const listSources = (sessionId) => request.get(`/api/v1/sessions/${sessionId}/sources`)
