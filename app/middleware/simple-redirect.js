import {useMainStore} from "~/store/index.js";
import {useAuthStore} from "~/store/auth.js";
// import Cookie from "js-cookie";

export default defineNuxtRouteMiddleware((to, from, next) => {
  const authStore = useAuthStore()

  const { ies_data, is_logged, authCookie } = authStore
  // console.log("is_logged", is_logged)
  // console.log("ies_data", ies_data)
  // console.log("authCookie", authCookie)

  // async function redirectLogic() {
  //   const user_data = await authStore.checkAuthSimple()
  // }

  if (to.path === '/') {
    // console.log('redirecting to dashboard')
    if (authCookie){
      // if (!is_logged){
      //   await redirectLogic()
      // }
      if (ies_data){
        return navigateTo('/respuestas')
      }
      else {
        return navigateTo('/dashboard')
      }
    }
    else{
      return navigateTo('/login')
    }
  }
})