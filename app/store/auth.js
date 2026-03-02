import { defineStore } from "pinia";
import { useIesStore } from '~/store/ies'

export const useAuthStore = defineStore("auth", {
  state: () => ({
    is_logged: false,
    auth_onigies: null,
    user_onigies: null,
    is_logging_in: true,
    dialog_login: false,
  }),
  actions: {
    setToken(token) {
      this.auth_onigies = token
    },
    setAuth(user, from_mid=true) {
      const iesStore = useIesStore()
      const { institution, institution_details, ...user_onigies } = user;
      this.user_onigies = user_onigies
      if (institution && institution_details)
        iesStore.setIesData(institution, institution_details)
      this.is_logged = Date.now()
      if (!from_mid){
        const token = useCookie('auth_onigies')
        token.value = user.token
      }
      this.auth_onigies = user.token
    },
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
    async checkAuthSimple() {
      if (this.auth_onigies) {
        return this.getLogin()
      }
      return new Promise((resolve) => {
        if (this.is_logged) {
          let last_login = this.is_logged
          if (!!last_login && last_login + (3600*24*1000) > Date.now()){
            this.purgeAuth()
            return resolve()
          }
        }
        else if (cookie_auth.value) {
          this.auth_onigies = cookie_auth.value
          return this.getLogin()
        }
        else {
          return resolve()
        }
        return resolve(this.getCurrentUser())
      })
    },
    getCurrentUser() {
      console.log("getCurrentUser", this.user_onigies)
      if (this.user_onigies){
        return this.user_onigies
      }
      else{
        return null
      }
    },
    getLogin() {
      return new Promise((resolve) => {
        const { $api } = useNuxtApp()
        $api.get('/login/')
          .then(({data, status}) => {
            if (status !== 204){
              console.log("LOGIN_DATA", data)
              this.hasLogged(data)
              return resolve(data)
            }
            else{

              this.hasNotLogged('Not Content (204)')
              return resolve(null)
            }
          })
          .catch(err =>{
            console.log("LOGIN_ERROR", err)
            this.hasNotLogged(`Server error: ${err}`)
            return resolve(null)
          })
      })
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
    },
    purgeAuth(from_mid=true) {
      const iesStore = useIesStore()
      // console.log("purgeAuth")
      this.user_onigies = null
      this.auth_onigies = null
      iesStore.purgeIesData()
      if (!from_mid){
        const token = useCookie('auth_onigies')
        token.value = null
      }
    },
    logout() {
      const router = useRouter()
      this.purgeAuth(false)
      return router.push({ path: '/login' })
    },
    async requestPasswordReset(email) {
      const { $api } = useNuxtApp()
      return await $api.post('/password-recovery/', { email })
    },
    async validateResetToken(token) {
      const { $api } = useNuxtApp()
      // return await $api.get(`/password-recovery/${token}/`)
      const { data } = await $api.get(`/password-recovery/${token}/`)
      return data
    },
    async confirmNewPassword(token, password, password_confirm) {
      const { $api } = useNuxtApp()
      const { data } = await $api.post(
        `/password-recovery/${token}/confirm/`, { password, password_confirm }
      )
      this.hasLogged(data, false)
      return data
    },
    async registerWithInvitation(uuid, userData) {
      const { $api } = useNuxtApp()
      const { data } = await $api.post(`/invitation/${uuid}/register/`, userData)
      this.hasLogged(data, false)
      return data
    },
    async getInvitation(uuid) {
      const { $api } = useNuxtApp()
      return await $api.get(`/invitation/${uuid}/`)
    },
    async listInvitations(institution_id) {
      const { $api } = useNuxtApp()
      const { data } = await $api.get('/invitation/', 
        { params: { institution: institution_id } })
      return data
    },
    async createInvitation(payload) {
      const { $api } = useNuxtApp()
      const { data } = await $api.post('/invitation/', payload)
      return data
    },
    async deleteInvitation(uuid) {
      const { $api } = useNuxtApp()
      await $api.delete(`/invitation/${uuid}/`)
    },
  },
  getters: {
    authCookie(state) {
      return state.auth_onigies
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