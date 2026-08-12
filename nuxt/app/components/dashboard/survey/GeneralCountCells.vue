<script setup>
/**
 * Celdas de conteo por sexo y género compartidas por las dos tablas matriz
 * de «Información base» (poblaciones y autoridades): los tres conteos más el
 * total. Emite `<td>` sueltos (raíz fragmento), así que solo vive dentro de
 * un `<tr>`; la fila dueña decide todo lo demás (presencia, «No aplica»,
 * columnas propias) y le pasa aquí solo lo resuelto, como `disabled`.
 */
const props = defineProps({
  // Fila de PopulationQuantity del sector; sus conteos se editan en sitio.
  row: { type: Object, required: true },
  // Sector del catálogo: da el `id` de las claves de error y el nombre de
  // los aria-labels.
  sector: { type: Object, required: true },
  editable: { type: Boolean, default: false },
  // Ya resuelto por la tabla dueña: cada una tiene su propio criterio de
  // contable (presencia en poblaciones, `no_apply` en autoridades).
  disabled: { type: Boolean, default: false },
  showNonBinary: { type: Boolean, default: false },
  // Claves de la compuerta de completado (useGeneralValidation).
  invalid: { type: Set, default: () => new Set() },
  total: { type: Number, default: null },
})

// Mujeres antes que Hombres: convención de columnas de todo ONIGIES.
const COUNT_FIELDS = [
  { field: 'number_women', label: 'Mujeres' },
  { field: 'number_men', label: 'Hombres' },
  { field: 'number_non_binary', label: 'No binarie' },
]

const fields = computed(() => props.showNonBinary
  ? COUNT_FIELDS : COUNT_FIELDS.slice(0, 2))

const countError = (field) =>
  props.invalid.has(`count:${props.sector.id}:${field}`)
</script>

<template>
  <td v-for="{ field, label } in fields" :key="field" class="text-right">
    <v-count-input
      v-model="row[field]"
      :readonly="!editable"
      :disabled="disabled"
      :error="countError(field)"
      :aria-label="`${label} — ${sector.name}`"
      inputmode="numeric"
    />
  </td>
  <td class="text-right text-body-1 font-weight-medium">
    {{ total ?? '—' }}
  </td>
</template>
