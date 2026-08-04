<script setup>
/**
 * Entero no negativo con la convención de la sección «Información base»:
 * alineado a la derecha, sin decimales y sin los controles de incremento
 * (capturar 4 320 personas a golpe de flecha no tiene sentido).
 */
defineProps({
  label: { type: String, default: '' },
  readonly: Boolean,
  disabled: Boolean,
  density: { type: String, default: 'comfortable' },
  hideDetails: { type: [Boolean, String], default: 'auto' },
})

const value = defineModel({ type: Number, default: null })
</script>

<template>
  <v-number-input
    v-model="value"
    :label="label"
    :readonly="readonly"
    :disabled="disabled"
    :density="density"
    :hide-details="hideDetails"
    :precision="0"
    :min="0"
    :step="1"
    control-variant="hidden"
    variant="outlined"
    class="general-number"
  />
</template>

<style scoped>
.general-number :deep(input) {
  text-align: right;
}
</style>
