<script setup>
import LoginCard from '~/components/login/LoginCard.vue'
import RegisterForm from '~/components/login/RegisterForm.vue'

definePageMeta({ layout: 'login' })

const route = useRoute()
const card = ref(null)
const uuid = computed(() => route.query.token || '')
</script>

<template>
  <LoginCard
    ref="card"
    title="Crea tu usuario"
    subtitle="Agrega un correo electrónico y contraseña"
  >
    <RegisterForm
      :uuid="uuid"
      @set-alert="card.setAlert($event)"
    />
  </LoginCard>
</template>