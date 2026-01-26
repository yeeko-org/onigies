<script setup>

const route = useRoute()
import { useAuthStore } from "~/stores/auth.js";
import SectionTitle from "~/components/login/SectionTitle.vue";
import LoginMail from "~/components/login/LoginMail.vue";
const authStore = useAuthStore();


definePageMeta({
  layout: 'login',
})

const props = defineProps({
  is_reset: {
    type: Boolean,
    required: false,
    default: false,
  },
  is_init: {
    type: Boolean,
    required: false,
    default: false,
  }
})
const alert_error = ref(false)
const error_message = ref(undefined)
const login_mail = ref(undefined)
const want_recovery = ref(false)
const login_mail_comp = ref("LoginMail")

function setAlert(message){
  alert_error.value = !!message
  error_message.value = message
    ? typeof(message) == 'object'
      ? message.detail || message
      : JSON.stringify(message)
    : '---'
}

function wantRecovery(val=true){
  setAlert(false)
  want_recovery.value = val
}

onMounted(()=>{
  console.log("route query token:", route)
  if (!route.query.token)
    setAlert("Para registrarse es necesario un token de invitación")
  authStore.checkValidationToken(route.query.token)
})


</script>

<template>
  <v-row class="d-flex justify-center align-center text-center">
    <v-card
      width="620"
      class="mt-6 rounded-shaped mb-3"
      color="#bfe0de"
    >
      <div class="no-wrap my-3 pt-3">
        <SectionTitle
          title="Crea tu usuario"
        />
        <div class="text-h6 text-grey-darken-1 my-2">
          Agrega un correo electrónico y contraseña
        </div>
      </div>
      <v-alert
        type="error"
        :model-value="alert_error"
        border="bottom"
        transition="scale-transition"
        class="mx-3"
      >{{error_message}}</v-alert>
<!--      <ResetPassword-->
<!--        v-if="texts.component === 'ResetPassword'"-->
<!--        @set-alert="setAlert($event)"-->
<!--        :want_recovery="want_recovery"-->
<!--        :is_init="is_init"-->
<!--      ></ResetPassword>-->
      <LoginMail
        ref="login_mail"
        @set-alert="setAlert($event)"
        :want_recovery="want_recovery"
        @want-recovery="wantRecovery($event)"
      />
    </v-card>
  </v-row>
</template>

<style scoped>
.no-wrap{
  word-break: normal !important;
}
</style>
