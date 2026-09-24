<script setup>
/**
 * Bloque de transversalidad sectorial: a qué poblaciones alcanza la
 * medida. Donde la pregunta ofrece la salida de planeación general, al
 * marcarla los sectores dejan de aplicar (`not_focalized`).
 */
const props = defineProps({
  observable: { type: Object, required: true },
  readonly: Boolean,
  disabled: Boolean,
})

const draft = defineModel({ type: Object, required: true })

// Los sectores llegan en su `order` desde el backend: no se reordenan.
const questions = computed(() => props.observable.reach_questions || [])
</script>

<template>
  <div>
    <div v-for="question in questions" :key="question.id" class="mb-2">
      <p class="text-body-1 font-weight-medium mb-2">
        {{ question.text }}
      </p>
      <template v-if="draft[question.id]">
        <v-checkbox
          v-if="question.has_general_planning"
          v-model="draft[question.id].not_focalized"
          label="Cubierto por la planeación general"
          :readonly="readonly"
          :disabled="disabled"
          color="accent"
          density="compact"
          hide-details
          class="mb-1"
        />
        <div class="cp-reach-grid">
          <v-checkbox
            v-for="sector in question.sectors"
            :key="sector.id"
            v-model="draft[question.id].sectors"
            :value="sector.id"
            :label="sector.name"
            :readonly="readonly"
            :disabled="disabled || draft[question.id].not_focalized"
            color="accent"
            density="compact"
            hide-details
          />
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.cp-reach-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  column-gap: 16px;
}
</style>
