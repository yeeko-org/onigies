<script setup>

import { useIesStore } from "~/store/ies.js";
const iesStore = useIesStore()

definePageMeta({
  middleware: 'dashboard',
  layout: 'ies',
})
const route = useRoute()
watch(
  () => route.params.period,
  (val) => {
    // if (!val) return
    // console.log('Route period changed:', val)
    iesStore.setCurrentPeriod(val)
  },
  { immediate: true }
)
</script>

<template>
  <NuxtPage/>
</template>

<style scoped>

</style>