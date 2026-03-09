<script setup>
const password = defineModel({ type: String, default: '' })

const props = defineProps({
  label: { type: String, default: 'Contraseña' },
  rules: { type: Array, default: () => [] },
})

const show_password = ref(false)
</script>

<template>
  <v-text-field
    v-model="password"
    :type="show_password ? 'text' : 'password'"
    :label="label"
    :rules="rules"
    variant="solo"
    :append-inner-icon="show_password ? 'visibility' : 'visibility_off'"
    @click:append-inner="show_password = !show_password"
  >
    <template #prepend-inner>
      <v-icon color="#de6eea">lock</v-icon>
    </template>
  </v-text-field>
</template>
