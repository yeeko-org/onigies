<script setup>
/**
 * Pregunta de Sí/No en una fila: el texto a la izquierda con ancho fijo y
 * los radios a la derecha en una columna también fija, siempre en
 * horizontal y con «Sí» primero. Con varias filas seguidas los radios
 * quedan alineados en columna sin importar el largo de cada texto.
 *
 * `readonly` y `disabled` son distintos a propósito: quien revisa lee la
 * respuesta con su contraste normal (readonly); lo apagado (disabled) es
 * para lo que todavía no se puede responder.
 *
 * `options` permite escalas propias con la misma forma (p. ej. las opciones
 * globales de A, cuyos valores son ids); llegan ya en el orden a pintar.
 */
const props = defineProps({
  label: { type: String, default: '' },
  options: {
    type: Array,
    default: () => [
      { value: true, text: 'Sí' },
      { value: false, text: 'No' },
    ],
  },
  readonly: Boolean,
  disabled: Boolean,
  labelClass: { type: String, default: 'text-body-2' },
  labelWidth: { type: Number, default: 560 },
  radiosWidth: { type: Number, default: 180 },
})

const value = defineModel({ type: [Boolean, Number, String], default: null })
</script>

<template>
  <div class="yes-no d-flex align-center ga-4">
    <div
      class="yes-no__label"
      :class="labelClass"
      :style="{ flexBasis: `${labelWidth}px`, maxWidth: `${labelWidth}px` }"
    >
      <slot name="label">{{ label }}</slot>
    </div>
    <v-radio-group
      v-model="value"
      :readonly="readonly"
      :disabled="disabled"
      :aria-label="label || undefined"
      color="accent"
      density="compact"
      inline
      hide-details
      class="yes-no__radios"
      :style="{ flexBasis: `${radiosWidth}px`, width: `${radiosWidth}px` }"
    >
      <v-radio
        v-for="option in options"
        :key="String(option.value)"
        :label="option.text"
        :value="option.value"
      />
    </v-radio-group>
    <slot name="append" />
  </div>
</template>

<style scoped>
.yes-no__label {
  flex-grow: 0;
  flex-shrink: 1;
  min-width: 0;
}
.yes-no__radios {
  flex-grow: 0;
  flex-shrink: 0;
}
/* Aire entre opciones: pegadas, «Sí» y «No» se leen como una sola
   etiqueta y el clic cae en la equivocada. */
.yes-no__radios :deep(.v-selection-control-group) {
  column-gap: 16px;
}
</style>
