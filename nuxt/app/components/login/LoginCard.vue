<script setup>
import SectionTitle from '~/components/login/SectionTitle.vue'

defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
})

const alert_error = ref(false)
const error_message = ref('')

function setAlert(message) {
  alert_error.value = !!message
  error_message.value = message
    ? typeof message === 'object'
      ? message.detail || JSON.stringify(message)
      : message
    : ''
}

defineExpose({ setAlert })
</script>

<template>
  <v-row class="d-flex justify-center align-center text-center">
    <v-card
      width="600"
      class="mt-6 rounded-shaped mb-3"
      color="#bfe0de"
    >
      <div class="no-wrap my-3 pt-3">
        <SectionTitle :title="title" />
        <div v-if="subtitle" class="text-h6 text-grey-darken-1 my-2">
          {{ subtitle }}
        </div>
      </div>
      <v-alert
        type="error"
        :model-value="alert_error"
        border="bottom"
        transition="scale-transition"
        class="mx-3"
      >{{ error_message }}</v-alert>
      <div style="max-width: 450px;" class="mx-auto mb-4">

        <slot />
      </div>
    </v-card>
  </v-row>
</template>

<style scoped>
.no-wrap {
  word-break: normal !important;
}
</style>