<script setup>
import GoodPracticeEditSimple from "~/components/dashboard/example/good_practice/GoodPracticeEditSimple.vue";
import GoodPracticeIntro from "~/components/dashboard/example/good_practice/GoodPracticeIntro.vue";

// Envoltura presentacional del diálogo de edición de una práctica.
// El v-model lleva el objeto vivo (la misma referencia que el padre): la
// edición de contenido y la sincronización de status/flow_events las
// gobierna el padre; aquí solo se abre/cierra y se reemiten saved/deleted.
const practice = defineModel({ default: null })

defineProps({
  isStaff: { type: Boolean, default: false },
  editable: { type: Boolean, default: false },
  title: { type: String, default: 'Editar Buena Práctica' },
})

const emit = defineEmits(['saved', 'deleted', 'transitioned'])

function close() {
  practice.value = null
}
</script>

<template>
  <v-dialog
    :model-value="!!practice"
    @update:model-value="close"
    scrollable
    max-width="1000"
  >
    <GoodPracticeEditSimple
      v-if="practice"
      v-model="practice"
      :is-staff="isStaff"
      :editable="editable"
      class="mt-3"
      @saved="emit('saved', $event)"
      @deleted="emit('deleted', $event)"
      @transitioned="emit('transitioned', $event)"
      @close="close"
    >
      <template #header>
        <v-toolbar color="primary">
          <v-toolbar-title>{{ title }}</v-toolbar-title>
          <v-spacer />
          <GoodPracticeIntro>
            <template #activator="{ props: activatorProps }">
              <v-btn
                v-bind="activatorProps"
                variant="text"
                color="white"
                prepend-icon="help_outline"
              >
                ¿Qué es una buena práctica?
              </v-btn>
            </template>
          </GoodPracticeIntro>
          <v-spacer />
          <v-btn icon @click="close">
            <v-icon>close</v-icon>
          </v-btn>
        </v-toolbar>
      </template>
    </GoodPracticeEditSimple>
  </v-dialog>
</template>