import axios from 'axios'
import { useAuthStore } from '~/store/auth.js'

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

  // Un 401 fuera del login significa sesión perdida (cookie borrada o
  // vencida con el store aún en memoria): se purga todo y se manda a
  // /login en vez de pintar el JSON del API en la pantalla.
  api.interceptors.response.use(undefined, (error) => {
    const status = error?.response?.status
    const url = error?.config?.url || ''
    const is_auth_call = url.includes('/login')
    if (status === 401 && !is_auth_call && import.meta.client) {
      useAuthStore(nuxtApp.$pinia).purgeAuth(false)
      navigateTo({ path: '/login', query: { expired: '1' } })
    }
    return Promise.reject(error)
  })
  return {
    provide: {
      api: api
    }
  }
})
