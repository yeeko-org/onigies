<script setup>
/**
 * Renglón compartido por las cinco familias de preguntas por
 * observable. Ninguna tiene `name_field`, así que el título genérico
 * saldría «SIN NOMBRE/TÍTULO»: aquí manda el texto de la pregunta, que
 * es justo lo que quien corrige el instrumento busca.
 *
 * Lo envuelve un `{Model}Header.vue` por tipo; la convención de nombre
 * no resuelve este archivo.
 */
import HeaderCommon from "~/components/dashboard/common/generic/HeaderCommon.vue";

const props = defineProps({
  main: Object,
  collection_data: Object,
  show_details: {
    type: Boolean,
    default: false,
  },
  chips: {
    type: Array,
    default: () => [],
  },
})

</script>

<template>
  <HeaderCommon
    :main="main"
    :show_details="show_details"
    :collection_data="collection_data"
    :width="460"
  >
    <template #title>
      {{ main.text }}
    </template>
    <template #details>
      <v-chip
        v-for="chip in chips"
        :key="chip"
        size="small"
        variant="tonal"
        color="grey-darken-2"
        class="mr-1"
      >
        {{ chip }}
      </v-chip>
    </template>
  </HeaderCommon>
</template>

<style scoped>

</style>
