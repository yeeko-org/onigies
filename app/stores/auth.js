import { defineStore } from "pinia";
// import Cookie from "js-cookie";
import { useIesStore } from '~/stores/ies'

export const useAuthStore = defineStore("auth", {
  state: () => ({
    is_authenticated: false,
    is_logged: false,
    auth_onigies: null,
    user_onigies: null,
    is_logging_in: true,
    dialog_login: false,
    ies_data: null,
  }),
  actions: {
    setToken(token) {
      this.auth_onigies = token
      //ApiService.defaults.headers.common['Authorization'] = `Token ${token}`;
      //ApiService.defaults.headers.common['Authorization
    },
    setAuth(user, from_mid=true) {
      const iesStore = useIesStore()
      // console.log("setAuth")
      const { institution, ...user_onigies } = user;
      this.is_authenticated = true
      this.user_onigies = user_onigies
      iesStore.setIesData(user.institution || null)
      this.is_logged = Date.now()
      this.is_logging_in = false
      // Cookie.set('auth_onigies', user.token)
      // console.log("Cookie", Cookie)
      // console.log("auth_onigies", Cookie.get('auth_onigies'))
      if (!from_mid){
        const token = useCookie('auth_onigies')
        token.value = user.token
      }
      this.auth_onigies = user.token
    },
    // setHeader() {
    //   if (this.auth_onigies) {
    //     let token = this.auth_onigies
    //     ApiService.defaults.headers.common['Authorization'] = `Token ${token}`
    //   }
    // },
    checkValidationToken(token) {
      const { $api } = useNuxtApp()
      return new Promise((resolve) => {
        $api.post(`/login/validate_token/${token}/`)
          .then(({data, status}) => {
            if (status !== 204)
              return resolve({valid: true, data: data})
            else
              return resolve({valid: false, error: 'Not Content (204)'})
          })
          .catch(err =>{
            console.log("VALIDATE_TOKEN_ERROR", err)
            return resolve({valid: false,  error: `Server error: ${err}`})
          })
      })
    },
    checkAuthSimple() {
      // const cookie_auth = Cookie.get('auth_onigies')
      const cookie_auth = useCookie('auth_onigies')

      // console.log("checkAuthSimple")
      return new Promise((resolve) => {
        if (this.is_logged) {
          // console.log("hay auth", this.auth_onigies)
          let last_login = this.is_logged
          if (!!last_login && last_login + (3600*24*1000) > Date.now()){
            // console.log("NO hay datos recientes")
            this.purgeAuth()
            return resolve()
          }
          else{
            // console.log("hay datos recientes")
          }
        }
        else if (cookie_auth.value) {
          // console.log("hay cookie", this.auth_onigies)
          this.auth_onigies = cookie_auth.value
          // this.setHeader()
          this.getLogin()
        }
        else {
          // console.log("NO ESTÁ LOGUEADO")
          return resolve()
        }
        return resolve(this.getCurrentUser())
      })
    },
    getCurrentUser() {
      if (this.user_onigies){
        return this.user_onigies
      }
      else{
        // console.log("en el nuxt no hay datos del usuario")
        return null
      }
    },
    getLogin() {
      // console.log("getLogin")
      // return new Promise((resolve) => {
      // this.setHeader()
      const { $api } = useNuxtApp()
      $api.get('/login/')
        .then(({data, status}) => {
          if (status !== 204)
            return this.hasLogged(data)
          else
            return this.hasNotLogged('Not Content (204)')
        })
        .catch(err =>{
          console.log("LOGIN_ERROR", err)
          return this.hasNotLogged(`Server error: ${err}`)
        })
      // })
    },
    loginMail(params) {
      const { $api } = useNuxtApp()
      return new Promise((resolve) => {
        $api.post('/login/', params)
          .then(({data}) => {
            this.hasLogged(data, false)
            return resolve(data)
          })
          .catch(err =>{
            return resolve({error:err})
          })
      })
    },
    hasLogged(userData, from_mid=true) {
      this.purgeAuth(from_mid)
      this.setAuth(userData, from_mid)
      // if (userData.profile && userData.profile.organization){
      //   console.log("seteamos la organización")
      //   commit("arropa/SET_ORGANIZATION_ID", userData.profile.organization.id, {root: true})
      // }
      if (!from_mid){
        this.redirectLogin(userData.is_ies)
      }
    },
    hasNotLogged(error) {
      this.is_logging_in = false
      console.error(error)
      this.purgeAuth()
      return null
    },
    redirectLogin(is_ies=false) {
      const router = useRouter()
      if (is_ies)
        return router.push({ path: '/respuestas'})
      else
        return router.push({ path: '/dashboard'})
      // return $router.push({ path: '/dashboard'})
    },
    purgeAuth(from_mid=true) {
      // console.log("purgeAuth")
      this.is_authenticated = false
      this.user_onigies = null
      this.auth_onigies = null
      this.ies_data = null
      // Cookie.remove('auth_onigies')
      if (!from_mid){
        const token = useCookie('auth_onigies')
        token.value = null
      }
    },
    logout() {
      const router = useRouter()
      // const route = useRoute()
      this.purgeAuth(false)
      return router.push({ path: '/login' })
    }
  },
  getters: {
    authCookie() {
      // console.log("Cookie", Cookie)
      // console.log("authCookie", Cookie.get('auth_onigies'))
      const token = useCookie('auth_onigies')
      return token.value
      // return true
    },
    is_staff(state) {
      if (state.user_onigies)
        return state.user_onigies.is_staff || false
    },
    is_full_editor(state) {
      if (state.user_onigies)
        return state.user_onigies.is_full_editor || state.user_onigies.is_staff || false
      return false
    },
    is_mini_editor(state) {
      if (state.user_onigies)
        return state.user_onigies.is_mini_editor || false
      return false
    }
  }

});