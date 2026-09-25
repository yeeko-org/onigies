<script setup>
/**
 * Split-button de guardado de un objeto del flujo: «Guardar ▾» abre un menú
 * encabezado por «Guardar y mantener como {status}» y seguido de cada
 * transición disponible, que el padre resuelve guardando primero y
 * transicionando después. Sin transiciones queda un «Guardar» simple.
 *
 * Presentacional: quien lo monta aporta el guardado (`@save`), el
 * guardar-y-transicionar (`@select`) y los diálogos del kernel
 * (FlowTransitionDialogs), igual que los split-buttons de gen y bp.
 */
import FlowTransitionMenu from
  '~/components/dashboard/flow/FlowTransitionMenu.vue'

defineProps({
  transitions: { type: Array, default: () => [] },
  // Status actual resuelto del catálogo, para nombrar el guardado simple.
  currentStatus: { type: Object, default: null },
  loading: Boolean,
  disabled: Boolean,
  // Apaga solo el guardado simple (p. ej. sin cambios que guardar); las
  // transiciones siguen disponibles.
  saveDisabled: Boolean,
  // Reemplaza «Guardar y mantener como …» cuando guardar no mantiene el
  // status (p. ej. cp, cuyo primer guardado promueve a «En llenado»).
  saveLabel: { type: String, default: '' },
})

const emit = defineEmits(['save', 'select'])
</script>

<template>
  <v-btn
    v-if="!transitions.length"
    variant="flat"
    prepend-icon="save"
    :loading="loading"
    :disabled="disabled || saveDisabled"
    @click="emit('save')"
  >
    Guardar
  </v-btn>
  <v-menu v-else location="bottom end">
    <template #activator="{ props: menuProps }">
      <v-btn
        v-bind="menuProps"
        variant="flat"
        prepend-icon="save"
        append-icon="expand_more"
        :loading="loading"
        :disabled="disabled"
      >
        Guardar
      </v-btn>
    </template>
    <FlowTransitionMenu
      :transitions="transitions"
      @select="(t) => emit('select', t)"
    >
      <template #lead>
        <v-list-item
          :title="saveLabel
            || `Guardar y mantener como ${currentStatus?.public_name}`"
          :disabled="saveDisabled"
          @click="emit('save')"
        >
          <template #prepend>
            <v-icon color="accent">save</v-icon>
          </template>
        </v-list-item>
        <v-divider />
      </template>
    </FlowTransitionMenu>
  </v-menu>
</template>
