<script setup>
import authMix from '~/components/login/auth_mix.js'
import { useAuthStore } from '~/store/auth.js'

const { rules } = authMix
const authStore = useAuthStore()
const emits = defineEmits(['set-alert'])

const email = ref('')
const loading = ref(false)
const sent = ref(false)
const form_ref = ref(null)

async function requestReset() {
  const { valid } = await form_ref.value.validate()
  if (!valid) return
  loading.value = true
  try {
    await authStore.requestPasswordReset(email.value)
    sent.value = true
    emits('set-alert', false)
  } catch (err) {
    emits('set-alert', err.response?.data || 'Error al enviar el correo.')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-card-text>
    <v-alert
      v-if="sent"
      type="success"
      variant="tonal"
      class="mb-4 text-left"
    >
      Si el correo existe, recibirás un enlace en breve.
    </v-alert>
    <v-form ref="form_ref" class="d-flex flex-column align-center">
      <v-text-field
        v-model="email"
        label="Correo electrónico"
        type="email"
        variant="solo"
        :rules="[rules.email, rules.user_name]"
        style="width: 450px;"
      >
        <template #prepend-inner>
          <v-icon color="#de6eea">mail</v-icon>
        </template>
      </v-text-field>
    </v-form>
  </v-card-text>
  <v-card-actions
    class="mb-4 mx-3"
    style="width: 450px;"
  >
    <v-btn
      text
      color="accent"
      :to="{ name: 'login' }"
    >
      Volver
    </v-btn>
    <v-spacer />
    <v-btn
      color="accent"
      variant="elevated"
      :loading="loading"
      :disabled="sent"
      @click="requestReset"
    >
      Enviar correo
    </v-btn>
  </v-card-actions>
</template>