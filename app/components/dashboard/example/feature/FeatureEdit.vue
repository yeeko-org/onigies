<script setup >

const props = defineProps({
  is_massive_edit: Boolean,
  is_edit: Boolean,
})
const full_main = defineModel({type: Object, required: true})
</script>

<template>
  <v-col cols="12" class="d-flex pa-0">

    <v-textarea
      v-model="full_main.reason_text"
      label="Texto para justificar la calificación"
      rows="2"
      variant="outlined"
      auto-grow
    >
    </v-textarea>

  </v-col>
</template>

<style scoped>

</style>