<script setup >

const props = defineProps({
  is_massive_edit: Boolean,
  is_edit: Boolean,
})

const full_main = defineModel({type: Object, required: true})

</script>

<template>
  <v-col cols="12" class="d-flex pa-0">
    <v-text-field
      v-model="full_main.year"
      label="Año (YYYY)"
      type="number"
      class="mr-2"
      variant="outlined"
      style="max-width: 300px;"
      readonly
    ></v-text-field>
  </v-col>
</template>

<style scoped>

</style>