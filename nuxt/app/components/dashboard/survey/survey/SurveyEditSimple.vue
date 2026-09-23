<script setup>
/**
 * Centro de control de la revisión sobre un cuestionario: monta la misma
 * sección «Información base» que captura la IES, en solo lectura, y debajo
 * los ejes del cuestionario principal con acceso a la revisión de cada uno.
 *
 * No duplica nada: `GeneralGroupList` ya es de doble audiencia y resuelve por
 * sí mismo el rol (auth), la editabilidad y las transiciones que le tocan a
 * cada quien. Aquí solo se le entrega el Survey completo —el EditSimple del
 * dashboard recibe únicamente `v-model`— para que no repita la petición: el
 * detalle ya trae anidado el `general_package` con sus grupos y su flujo.
 */
import GeneralGroupList from
  '~/components/dashboard/survey/GeneralGroupList.vue'
import CpSurveyAxes from
  '~/components/dashboard/answer/review/CpSurveyAxes.vue'

const full_main = defineModel({ type: Object, required: true })

const emit = defineEmits(['item-saved'])

/**
 * El renglón colapsado (SurveyHeader) lee el `general_package` del payload de
 * LISTA, un objeto distinto al del detalle: las mutaciones en sitio del kernel
 * de flujo no lo alcanzan. Se reenvía el resumen por `item-saved`, el canal
 * que PanelList ya usa para fusionar detalle en fila.
 */
function onFlowChanged(general_package) {
  emit('item-saved', {
    res: { id: full_main.value.id, general_package },
    is_new: false,
  })
}

const context = computed(() => {
  const inst = full_main.value.institution_full
  return `${inst?.acronym || inst?.name || ''} - ${full_main.value.period}`
})
</script>

<template>
  <div>
    <GeneralGroupList
      :survey="full_main"
      @flow-changed="onFlowChanged"
    />
    <CpSurveyAxes
      :axis-values="full_main.axis_values || []"
      :context="context"
    />
  </div>
</template>
