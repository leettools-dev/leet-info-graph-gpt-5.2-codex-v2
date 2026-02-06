import axios from 'axios'

const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const request = axios.create({
  baseURL: apiBase,
  timeout: 10000,
})

export default request
