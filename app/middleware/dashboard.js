import {useMainStore} from "~/store/index.js";
import {useAuthStore} from "~/store/auth.js";

export default defineNuxtRouteMiddleware((to, from, next) => {

  const mainStore = useMainStore()
  const authStore = useAuthStore()
  const cookieAuth = useCookie('auth_onigies')
  // console.log('FROM', from)
  const {
    fetchCatalogs,
    cats_ready,
    setCollection,
    setFilterGroup,
  } = mainStore

  if (cookieAuth.value && !authStore.auth_onigies) {
    authStore.setToken(cookieAuth.value)
  }
  // console.log("is_logged", is_logged)
  // console.log("authCookie", authCookie)
  // console.log("Cookie", useCookie())
  // if (!is_logged) {
  //   console.log('redirecting to login')
  //   return navigateTo('/login')
  // }
  if (!authStore.auth_onigies) {
    authStore.purgeAuth()
    return navigateTo('/login')
  }
  if (!authStore.is_logged) {
    authStore.checkAuthSimple()
  }

  if (to.params.group){
    setCollection(to.params.group)
  }
  else if (to.params.model)
    setFilterGroup(to.params.model)
  if (cats_ready) {
    // next()
    return
  }
  fetchCatalogs()
  // console.log('after cats')
  // console.log('after_check_auth')

  //   .then(() => {
  //   next()
  // })
  // console.log('Middleware dashboard.js called', to)
  // if (to.params.id === '1') {
  //   return abortNavigation()
  // }
  // In a real app you would probably not redirect every route to `/`
  // however it is important to check `to.path` before redirecting or you
  // might get an infinite redirect loop
})