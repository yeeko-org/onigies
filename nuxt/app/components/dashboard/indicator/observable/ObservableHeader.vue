<script setup>
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useMainStore } from "~/store/index.js";
import { useQuestionTypes } from "~/composables/useQuestionTypes.js";
import HeaderCommon from "~/components/dashboard/common/generic/HeaderCommon.vue";
import GenericDisplay from "~/components/dashboard/common/select/GenericDisplay.vue";
import HeaderChip from "~/components/dashboard/common/utils/HeaderChip.vue";
import TitleCommon from "~/components/dashboard/common/utils/TitleCommon.vue";

const props = defineProps({
  main: Object,
  collection_data: Object,
  show_details: {
    type: Boolean,
    default: false,
  },
})

const TITLE_WIDTH = 520
// Componente encima más dos líneas de título no caben en los 64 px por
// defecto de la fila.
const ROW_HEIGHT = 78

const QUESTION_UNIT = {label: 'pregunta', label_plural: 'preguntas'}

const TYPE_CHIPS = {
  a_questions: {
    collection_name: 'a_question', count_field: 'a_questions_count',
    ...QUESTION_UNIT},
  reach: {
    collection_name: 'reach_question', count_field: 'reach_sectors_count',
    label: 'sector', label_plural: 'sectores'},
  b_questions: {
    collection_name: 'b_question', count_field: 'b_questions_count',
    ...QUESTION_UNIT},
  plans: {
    collection_name: 'plan_question', count_field: 'plan_questions_count',
    ...QUESTION_UNIT},
  special: {
    collection_name: 'special_question',
    count_field: 'special_questions_count', hide_count: true,
    ...QUESTION_UNIT},
  population: {
    icon: 'diversity_3',
    color: 'deep-purple',
    is_reverse: true,
    tooltip_complement: 'Se captura en «Información de base».',
    ...QUESTION_UNIT,
  },
}

// Hay a lo más una BQuestion por observable: el conteo no informa, lo
// que distingue es a qué instancias se les pregunta.
const ORG_INSTANCES = [
  {key: 'b_includes_academic', icon: 'school', label: 'académicas'},
  {key: 'b_includes_admin', icon: 'apartment', label: 'administrativas'},
]

const { cats } = storeToRefs(useMainStore())
const { types_by_name } = useQuestionTypes()

const org_instances = computed(
  () => ORG_INSTANCES.filter(entry => props.main[entry.key]))

const org_tooltip = computed(() => org_instances.value.length === 2
  ? 'instancias académicas y administrativas'
  : `solo instancias ${org_instances.value[0]?.label}`)

const title_text = computed(() => `${props.main.number} ${props.main.name}`)

// El eje se resuelve por el componente: DisplayGroup no puede pintarlo
// solo, porque el observable no trae la llave `axis`.
const component = computed(() => (cats.value?.component || []).find(
  row => row.id === props.main.component) || null)

const axis_id = computed(() => component.value?.axis ?? null)

// `question_types` llega ordenado por QuestionType.order; no se reordena.
const counters = computed(() => (props.main.question_types || []).reduce(
  (acc, name) => {
    const chip = TYPE_CHIPS[name]
    if (chip)
      acc.push({
        name,
        ...chip,
        tooltip_title: types_by_name.value[name]?.public_name,
        count: chip.count_field ? props.main[chip.count_field] : 0,
      })
    return acc
  }, []))

</script>

<template>
  <HeaderCommon
    :main="main"
    :show_details="show_details"
    :collection_data="collection_data"
    :width="TITLE_WIDTH"
    :height="ROW_HEIGHT"
  >
    <template #icon>
      <GenericDisplay
        v-if="axis_id"
        :element_value="axis_id"
        level="group"
        :items="cats.axis"
        hide_border
      />
    </template>
    <template #title>
      <div>
        <div
          v-if="component"
          class="text-caption text-medium-emphasis text-truncate ml-2"
          :style="`max-width: ${TITLE_WIDTH}px;`"
        >
          {{ component.name }}
        </div>
        <TitleCommon
          :title_text="title_text"
          :title_width="TITLE_WIDTH"
        />
      </div>
    </template>
    <template #details>
      <div class="d-flex align-center ga-2">
        <HeaderChip
          v-for="counter in counters"
          :key="counter.name"
          :count="counter.count"
          :collection_name="counter.collection_name"
          :label="counter.label"
          :label_plural="counter.label_plural"
          :icon="counter.icon"
          :color="counter.color"
          :is_reverse="counter.is_reverse"
          :hide_count="counter.hide_count"
          :tooltip_title="counter.tooltip_title"
          :tooltip_complement="counter.tooltip_complement"
        >
          <template
            v-if="counter.name === 'b_questions' && org_instances.length"
            #content
          >
            <div class="d-flex align-center ga-1 px-1 py-1">
              <v-icon
                v-for="entry in org_instances"
                :key="entry.key"
                size="20"
              >
                {{ entry.icon }}
              </v-icon>
            </div>
          </template>
          <template
            v-if="counter.name === 'b_questions' && org_instances.length"
            #tooltip
          >
            <div class="font-weight-bold">
              {{ counter.tooltip_title }}: {{ org_tooltip }}
            </div>
          </template>
        </HeaderChip>
      </div>
    </template>
  </HeaderCommon>
</template>

<style scoped>

</style>
