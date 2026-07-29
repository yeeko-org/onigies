<script setup>
/**
 * Lista de transiciones disponibles (el contenido de un v-menu). Presentacional
 * puro: recibe las transiciones y emite la elegida. Lo reusan el chip-menú de
 * FlowStatusActions y el caret de los split-buttons de Guardar/Enviar.
 */
defineProps({
  transitions: { type: Array, required: true },
})
const emit = defineEmits(['select'])
</script>

<template>
  <v-list density="compact" min-width="260">
    <slot name="lead" />
    <!-- Con `blocked` (motivos de entry_rules/hijos calculados por el
         kernel) el ítem se pre-deshabilita y muestra los motivos como
         subtítulo, en vez de fallar al clic. -->
    <v-list-item
      v-for="t in transitions"
      :key="t.name"
      :title="t.action_name || t.public_name"
      :subtitle="t.blocked?.length ? t.blocked.join(' · ') : t.description"
      :disabled="!!t.blocked?.length"
      @click="emit('select', t)"
    >
      <template #prepend>
        <v-icon :color="t.color || 'primary'">
          {{ t.blocked?.length ? 'lock' : (t.icon || 'arrow_forward') }}
        </v-icon>
      </template>
    </v-list-item>
  </v-list>
</template>