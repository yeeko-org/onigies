<script setup>
/**
 * Muestra el status actual de un objeto del flujo. `status` es el nombre

 * (string, p. ej. "bp_draft"); el display (color/icon/public_name/description)
 * se resuelve desde el catálogo (useFlowStore), no viaja anidado en cada
 * objeto.
 *
 * El tooltip muestra public_name + description.
 */
import { useFlowStore } from '~/store/flow.js'

const props = defineProps({
  status:   { type: String, default: null },
  size:     { type: String, default: 'default' },
  label:    { type: String, default: '' },
  onlyIcon: Boolean,
  xSmall:   Boolean,
  disabled: Boolean,
})

const flowStore = useFlowStore()
const st = computed(() => flowStore.getStatus(props.status))
const chipSize = computed(() => (props.xSmall ? 'x-small' : props.size))
</script>

<template>
  <div v-if="st" class="d-inline-flex align-center ga-1">
    <span v-if="label" class="text-caption text-grey-darken-1">
      {{ label }}
    </span>
    <v-chip
      :color="st.color || 'grey'"
      :size="chipSize"
      :disabled="disabled"
      variant="elevated"
    >
      <v-icon :start="!onlyIcon">
        {{ st.icon || 'trip_origin' }}
      </v-icon>
      <template v-if="!onlyIcon">{{ st.public_name }}</template>
      <!-- Contenido opcional al final del chip (p. ej. caret cuando es un
           activador de menú en FlowStatusActions). -->
      <slot />
      <v-tooltip activator="parent" location="top">
        <div style="max-width: 300px;">
          <b>{{ st.public_name }}</b>
          <template v-if="st.description"><br>{{ st.description }}</template>
        </div>
      </v-tooltip>
    </v-chip>
  </div>
</template>