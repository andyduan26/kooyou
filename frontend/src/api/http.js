import axios from 'axios'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api',
  timeout: 15000
})

http.interceptors.response.use((response) => {
  const payload = response.data
  if (payload && Object.prototype.hasOwnProperty.call(payload, 'data')) {
    return payload.data
  }
  return payload
})

export default http
