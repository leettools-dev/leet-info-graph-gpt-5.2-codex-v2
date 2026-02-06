import request from '../utils/request'

export const loginWithGoogle = (credential) =>
  request.post('/api/v1/auth/google', { credential })

export const fetchCurrentUser = () => request.get('/api/v1/auth/me')

export const logout = () => request.post('/api/v1/auth/logout')
