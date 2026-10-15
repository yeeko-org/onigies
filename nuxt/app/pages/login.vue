<script setup>
import LoginCard from '~/components/login/LoginCard.vue'
import LoginMail from '~/components/login/LoginMail.vue'

definePageMeta({ layout: 'login' })

const card = ref(null)
const route = useRoute()

onMounted(() => {
  if (route.query.expired)
    card.value.setAlert('Tu sesión expiró; inicia sesión de nuevo.')
})
</script>

<template>
  <LoginCard ref="card" title="Inicia Sesión">
    <LoginMail @set-alert="card.setAlert($event)" />
  </LoginCard>
</template>
