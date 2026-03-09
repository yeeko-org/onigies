<script setup>
import LoginCard from '~/components/login/LoginCard.vue'
import ForgotPasswordForm from '~/components/login/ForgotPasswordForm.vue'

definePageMeta({ layout: 'login' })

const card = ref(null)
</script>

<template>
  <LoginCard
    ref="card"
    title="Recuperar contraseña"
    subtitle="Escribe tu correo electrónico"
  >
    <ForgotPasswordForm
      @set-alert="card.setAlert($event)"
    />
  </LoginCard>
</template>