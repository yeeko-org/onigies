<script setup>
/**
 * Sheet vacío a propósito.
 *
 * PanelCommon pinta el EditSimple y, siempre debajo, el slot #sheet. Sin
 * este override caería SheetCommon, que auto-listaría los
 * `observable_responses` del eje con su barra de filtros y paginación,
 * duplicando lo que ya muestra el cuestionario del eje.
 */
defineProps({
  full_main: Object,
  show_details: Boolean,
  collection_data: Object,
})
</script>

<template>
  <!-- Sin contenido: todo se muestra en el EditSimple. -->
</template>
