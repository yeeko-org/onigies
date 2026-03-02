<script setup>
import authMix from '~/components/login/auth_mix.js'
import { useAuthStore } from '~/store/auth.js'
import PasswordField from '~/components/login/PasswordField.vue'

const { rules } = authMix
const authStore = useAuthStore()
const { loginMail } = authStore

const emits = defineEmits(['set-alert'])

const form_ref = ref(null)
const login_form = ref(false)
const loading_login = ref(false)
const email = ref('')
const password = ref('')

async function sendLogin() {
  const { valid } = await form_ref.value.validate()
  if (!valid) return
  loading_login.value = true
  const res = await loginMail({ username: email.value, password: password.value })
  loading_login.value = false
  if (res?.error) {
    emits('set-alert', res.error.response?.data)
    password.value = ''
  } else {
    emits('set-alert', false)
  }
}
</script>

<template>
  <v-form
    ref="form_ref"
    v-model="login_form"
    class="d-flex flex-column align-center"
  >
    <v-card-text style="width: 450px;">
      <v-text-field
        v-model="email"
        label="Correo electrónico"
        name="email"
        variant="solo"
        type="email"
        :rules="[rules.email, rules.user_name]"
        class="mb-2"
      >
        <template #prepend-inner>
          <v-icon color="#de6eea">mail</v-icon>
        </template>
      </v-text-field>
      <PasswordField
        v-model="password"
        :rules="[rules.required, rules.min]"
        @keyup.enter="sendLogin"
      />
    </v-card-text>
    <v-card-actions
      class="mb-4 mx-3"
      style="width: 450px;"
    >
      <v-btn
        color="accent"
        variant="tonal"
        to="/forgot-password"
      >
        Recuperar contraseña
      </v-btn>
      <v-spacer />
      <v-btn
        color="accent"
        variant="elevated"
        :loading="loading_login"
        @click="sendLogin"
      >
        Iniciar sesión
      </v-btn>
    </v-card-actions>
  </v-form>
</template>