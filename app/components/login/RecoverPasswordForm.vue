<script setup>
import authMix from '~/components/login/auth_mix.js'
import { useAuthStore } from '~/store/auth.js'
import PasswordField from '~/components/login/PasswordField.vue'

const { rules } = authMix
const authStore = useAuthStore()
const emits = defineEmits(['set-alert'])

const props = defineProps({
  token: { type: String, required: true },
})
const subtitle = defineModel('subtitle', { type: String, required: false })

const form_ref = ref(null)
const password = ref('')
const password_confirm = ref('')
const token_valid = ref(false)
const token_loading = ref(true)
const loading = ref(false)

const confirm_rules = [
  rules.required,
  rules.min,
  (v) => v === password.value || 'Las contraseñas no coinciden',
]

onMounted(async () => {
  try {
    const res = await authStore.validateResetToken(props.token)
    console.log("validateResetToken res", res)
    token_valid.value = true
    subtitle.value = `Restablecer contraseña para ${res.email}`
  } catch (err) {
    token_valid.value = false
  } finally {
    token_loading.value = false
  }
})

async function confirmReset() {
  const { valid } = await form_ref.value.validate()
  if (!valid) return
  loading.value = true
  try {
    await authStore.confirmNewPassword(props.token, password.value, password_confirm.value)
  } catch (err) {
    const status = err.response?.status
    if (status === 400) {
      const data = err.response?.data
      // Token expired between step 2 and 3 (race condition)
      if (data?.non_field_errors || data?.token) {
        token_valid.value = false
      } else {
        emits('set-alert', data)
      }
    } else {
      emits('set-alert', err.response?.data || 'Error al restablecer la contraseña.')
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-card-text>
    <v-progress-linear v-if="token_loading" indeterminate color="accent" class="mb-4" />

    <template v-else-if="!token_valid">
      <v-alert type="warning" variant="tonal" class="mb-4 text-left">
        El enlace es inválido o ha expirado.
      </v-alert>
      <v-btn
        color="accent"
        variant="tonal"
        :to="'/forgot-password'"
        class="mb-4"
      >
        Solicitar nuevo enlace
      </v-btn>
    </template>

    <v-form v-else ref="form_ref" class="d-flex flex-column align-center">
      <PasswordField
        v-model="password"
        label="Nueva contraseña"
        :rules="[rules.required, rules.min]"
        style="width: 450px;"
      />
      <PasswordField
        v-model="password_confirm"
        label="Confirmar contraseña"
        :rules="confirm_rules"
        style="width: 450px;"
        @keyup.enter="confirmReset"
      />
    </v-form>
  </v-card-text>
  <v-card-actions v-if="!token_loading && token_valid" class="mb-4 mx-3 justify-end">
    <v-btn
      color="accent"
      variant="elevated"
      :loading="loading"
      @click="confirmReset"
    >
      Guardar contraseña
    </v-btn>
  </v-card-actions>
</template>