<script setup>
import authMix from '~/components/login/auth_mix.js'
import { useAuthStore } from '~/store/auth.js'
import PasswordField from '~/components/login/PasswordField.vue'

const { rules } = authMix
const authStore = useAuthStore()
const emits = defineEmits(['set-alert'])

const props = defineProps({
  uuid: { type: String, default: '' },
})

const form_ref = ref(null)
const first_name = ref('')
const last_name = ref('')
const email = ref('')
const password = ref('')
const password_confirm = ref('')
const loading = ref(false)
const invitation_valid = ref(false)
const institution = ref(null)

const confirm_rules = [
  rules.required,
  rules.min,
  (v) => v === password.value || 'Las contraseñas no coinciden',
]

onMounted(async () => {
  if (!props.uuid) return
  try {
    const { data } = await authStore.getInvitation(props.uuid)
    if (data.email) email.value = data.email
    if (data.institution_full) institution.value = data.institution_full
    invitation_valid.value = true
    emits('set-alert', false)
  } catch (err) {
    const status = err.response?.status
    if (status === 400)
      emits('set-alert', 'La invitación ya ha sido utilizada.')
    else if (status === 404)
      emits('set-alert', 'Invitación no encontrada.')
    else
      emits('set-alert', err.response?.data || 'Error al validar la invitación.')
  }
})

async function submitRegister() {
  const { valid } = await form_ref.value.validate()
  if (!valid) return
  loading.value = true
  try {
    await authStore.registerWithInvitation(props.uuid, {
      first_name: first_name.value,
      last_name: last_name.value,
      email: email.value,
      password: password.value,
      password_confirm: password_confirm.value,
    })
  } catch (err) {
    emits('set-alert', err.response?.data || 'Error al registrar el usuario.')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-form ref="form_ref" class="d-flex flex-column align-center">
    <v-card-text style="width: 450px;">
      <v-chip
        v-if="institution"
        color="primary"
        variant="tonal"
        prepend-icon="apartment"
        class="mb-4"
        label
      >
        <span class="font-weight-bold mr-1">{{ institution.acronym }}</span>
        {{ institution.name }}
      </v-chip>
      <v-text-field
        v-model="first_name"
        label="Nombre(s)"
        variant="solo"
        :rules="[rules.required]"
        class="mb-2"
      >
        <template #prepend-inner>
          <v-icon color="#de6eea">person</v-icon>
        </template>
      </v-text-field>
      <v-text-field
        v-model="last_name"
        label="Apellidos"
        variant="solo"
        :rules="[rules.required]"
        class="mb-2"
      >
        <template #prepend-inner>
          <v-icon color="#de6eea">person</v-icon>
        </template>
      </v-text-field>
      <v-text-field
        v-model="email"
        label="Correo electrónico"
        type="email"
        variant="solo"
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
        class="mb-2"
      />
      <PasswordField
        v-model="password_confirm"
        label="Confirmar contraseña"
        :rules="confirm_rules"
      />
    </v-card-text>
    <v-card-actions class="mb-4 mx-3" style="width: 450px;">
      <v-spacer />
      <v-btn
        color="accent"
        variant="elevated"
        :loading="loading"
        :disabled="!invitation_valid"
        @click="submitRegister"
      >
        Crear cuenta
      </v-btn>
    </v-card-actions>
  </v-form>
</template>
