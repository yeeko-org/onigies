<script setup>
/**
 * Fila de íconos del encabezado de un observable: uno por grupo de
 * respuesta, con el ícono del tipo de pregunta y el color del status del
 * grupo. Mismo lenguaje visual que los contadores del dashboard
 * (HeaderChip), sin el aviso de ausencia, que allá señala un faltante del
 * instrumento y aquí no aplica.
 */
import { useFlowStore } from '~/store/flow.js'
import { useQuestionTypes } from '~/composables/useQuestionTypes.js'
import HeaderChip from '~/components/dashboard/common/utils/HeaderChip.vue'

const props = defineProps({
  groups: { type: Array, default: () => [] },
  // Id del grupo que pide atención de la IES: su ícono se resalta.
  highlightId: { type: Number, default: null },
  dimmed: Boolean,
})

const flowStore = useFlowStore()
const { types_by_name } = useQuestionTypes()

const items = computed(() => props.groups.map((group) => {
  const type = types_by_name.value[group.question_type] || {}
  const status = flowStore.getStatus(group.status)
  return {
    id: group.id,
    icon: type.icon || 'help',
    typeName: type.public_name || group.question_type,
    color: status?.color || 'grey',
    statusName: status?.public_name || '',
    highlighted: group.id === props.highlightId,
  }
}))
</script>

<template>
  <div class="d-flex align-center ga-1" :class="{ 'cp-icons--dim': dimmed }">
    <HeaderChip
      v-for="item in items"
      :key="item.id"
      :color="item.color"
      :class="{ 'cp-icons--attention': item.highlighted }"
      horizontal
    >
      <template #content>
        <v-icon size="18" :color="item.color">{{ item.icon }}</v-icon>
      </template>
      <template #tooltip>
        <div class="font-weight-bold">{{ item.typeName }}</div>
        <div>{{ item.statusName }}</div>
      </template>
    </HeaderChip>
  </div>
</template>

<style scoped>
.cp-icons--dim {
  opacity: 0.4;
}
.cp-icons--attention {
  outline: 2px solid currentColor;
  outline-offset: 1px;
}
</style>
