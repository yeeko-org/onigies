<script setup>
/**
 * Bloque B (transversalidad orgánica): en cuántas instancias se cumple,
 * académicas y, si la pregunta las incluye, administrativas. El total que
 * la IES declaró en información base acompaña al campo como referencia.
 */
const props = defineProps({
  observable: { type: Object, required: true },
  genDenominators: { type: Object, default: () => ({}) },
  readonly: Boolean,
  disabled: Boolean,
})

const draft = defineModel({ type: Object, required: true })

const questions = computed(() => props.observable.b_questions || [])

const declared = (name) => props.genDenominators?.[name]?.value ?? null

function fieldsOf(question) {
  const fields = []
  if (question.includes_academic !== false)
    fields.push({
      key: 'academic_instances_complying',
      label: 'Instancias académicas',
      total: declared('academic_instances'),
    })
  if (question.includes_admin)
    fields.push({
      key: 'admin_instances_complying',
      label: 'Instancias administrativas',
      total: declared('admin_instances'),
    })
  return fields
}

const hint = (total) =>
  total === null ? '' : `de ${total} instancias declaradas`
</script>

<template>
  <div>
    <div v-for="question in questions" :key="question.id" class="mb-2">
      <p class="text-body-1 mb-3">{{ question.text }}</p>
      <div v-if="draft[question.id]" class="d-flex flex-wrap ga-6">
        <v-count-input
          v-for="field in fieldsOf(question)"
          :key="field.key"
          v-model="draft[question.id][field.key]"
          :label="field.label"
          :hint="hint(field.total)"
          :readonly="readonly"
          :disabled="disabled"
          persistent-hint
          hide-details="auto"
          inputmode="numeric"
          min-width="220"
          max-width="220"
        />
      </div>
    </div>
  </div>
</template>
