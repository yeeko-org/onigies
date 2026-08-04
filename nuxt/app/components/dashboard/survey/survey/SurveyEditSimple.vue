<script setup>
/**
 * Centro de control de la revisión sobre un cuestionario: monta la misma
 * sección «Información base» que captura la IES, en solo lectura.
 *
 * No duplica nada: `GeneralGroupList` ya es de doble audiencia y resuelve por
 * sí mismo el rol (auth), la editabilidad y las transiciones que le tocan a
 * cada quien. Aquí solo se le entrega el Survey completo —el EditSimple del
 * dashboard recibe únicamente `v-model`— para que no repita la petición: el
 * detalle ya trae anidado el `general_package` con sus grupos y su flujo.
 */
import GeneralGroupList from
  '~/components/dashboard/survey/GeneralGroupList.vue'

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
</script>

<template>
  <GeneralGroupList
    :survey="full_main"
    @flow-changed="onFlowChanged"
  />
</template>
