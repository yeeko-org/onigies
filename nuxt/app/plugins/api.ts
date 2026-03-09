import axios from 'axios'

export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig()
  const cookieAuth = useCookie('auth_onigies')

  const api = axios.create({
    baseURL: config.public.apiUrl,
    headers: {
      'Content-Type': 'application/json'
    }
  })

  api.interceptors.request.use((config) => {

    if (cookieAuth.value) {
      config.headers.Authorization = `Token ${cookieAuth.value}`
    }
    return config
  })
  return {
    provide: {
      api: api
    }
  }
})