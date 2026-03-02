<script setup>
import LoginCard from '~/components/login/LoginCard.vue'
import LoginMail from '~/components/login/LoginMail.vue'

definePageMeta({ layout: 'login' })

const card = ref(null)
</script>

<template>
  <LoginCard ref="card" title="Inicia Sesión">
    <LoginMail @set-alert="card.setAlert($event)" />
  </LoginCard>
</template>