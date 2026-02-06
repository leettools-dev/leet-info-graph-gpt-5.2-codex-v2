import request from '../utils/request'

export const fetchHealth = () => request.get('/api/v1/health')
