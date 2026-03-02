<script setup>
import LoginCard from '~/components/login/LoginCard.vue'
import RecoverPasswordForm from '~/components/login/RecoverPasswordForm.vue'

definePageMeta({ layout: 'login' })

const route = useRoute()
const card = ref(null)
const token = computed(() => route.query.token || '')
const subtitle = ref('')
</script>

<template>
  <LoginCard
    ref="card"
    title="Nueva contraseña"
    :subtitle="subtitle"
  >
    <RecoverPasswordForm
      :token="token"
      @set-alert="card.setAlert($event)"
      v-model:subtitle="subtitle"
    />
  </LoginCard>
</template>