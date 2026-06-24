<script setup>
/**
 * Indicador compacto (solo lectura) de que el objeto del flujo tiene
 * comentarios. Lee `flow_events` embebido —misma fuente que FlowComments—,
 * se muestra solo si hay algún comentario y delega el render del tooltip en
 * FlowTimeline (autor · fecha · texto), sin duplicar su lógica. No escribe;
 * el alta de comentarios vive en FlowComments dentro del detalle.
 */
import FlowTimeline from '~/components/dashboard/flow/FlowTimeline.vue'

const props = defineProps({
  events: { type: Array, default: () => [] },
})

const commentEvents = computed(() =>
  props.events.filter((ev) => ev.comment))
</script>

<template>
  <v-badge
    v-if="commentEvents.length"
    :content="commentEvents.length"
    color="yellow-darken-3"
    text-color="black"
    offset-x="2"
    offset-y="2"
  >
    <v-icon color="yellow-darken-3" class="align-self-center">
      sticky_note_2
    </v-icon>
    <v-tooltip activator="parent" location="top" content-class="pa-0">
      <v-card color="yellow-accent-4" class="pa-2" max-width="360">
        <div class="text-subtitle-2 font-weight-bold">
          Comentarios ({{ commentEvents.length }})
        </div>
        <FlowTimeline :events="commentEvents" />
      </v-card>
    </v-tooltip>
  </v-badge>
</template>