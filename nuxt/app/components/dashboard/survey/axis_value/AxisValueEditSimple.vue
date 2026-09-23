<script setup>
/**
 * Detalle de un eje para la revisión: el mismo cuestionario que captura
 * la IES (CpAxisCapture), en modo revisión. El contenido es de solo
 * lectura; quedan el status del eje, de cada observable y de cada grupo,
 * los comentarios y los adjuntos.
 *
 * El EditSimple del dashboard solo recibe `v-model`, y el detalle ya es
 * el de `/axis_value/{id}/`: se entrega el objeto para no repetir la
 * petición.
 */
import CpAxisCapture from
  '~/components/dashboard/answer/capture/CpAxisCapture.vue'

const full_main = defineModel({ type: Object, required: true })

const emit = defineEmits(['item-saved'])

// El renglón colapsado lee el objeto de LISTA, distinto del detalle: las
// mutaciones en sitio del kernel de flujo no lo alcanzan. Se reenvía el
// resumen por `item-saved`, el canal que PanelList fusiona en la fila.
function onFlowChanged(brief) {
  emit('item-saved', { res: brief, is_new: false })
}
</script>

<template>
  <CpAxisCapture
    :axis-value="full_main"
    review
    class="pa-2"
    @flow-changed="onFlowChanged"
  />
</template>
