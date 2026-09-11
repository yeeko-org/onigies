<script setup>
import { storeToRefs } from "pinia";
import { useTheme } from "vuetify";
import colors from "vuetify/lib/util/colors";
import { useMainStore } from "~/store/index.js";
import { useDashboardStore } from "~/store/dash.js";
import {
  deleteElement, patchElement, saveElement,
} from "~/composables/save_elements.js";
import { useQuestionTypes } from "~/composables/useQuestionTypes.js";
import ObservableQuestionEdit from
  "~/components/dashboard/question/common/ObservableQuestionEdit.vue";
import OrgInstancesFields from
  "~/components/dashboard/question/b_question/OrgInstancesFields.vue";
import ReachSectorFields from
  "~/components/dashboard/question/reach_question/ReachSectorFields.vue";
import DialogDelete from
  "~/components/dashboard/common/dialog/DialogDelete.vue";
import ConfirmActionDialog from
  "~/components/dashboard/common/dialog/ConfirmActionDialog.vue";

// Los defaults del tipo se calibraron para esta terna; en cualquier otra
// combinación no se hereda nada y hay que capturar fila por fila.
const STANDARD_TYPES = ['a_questions', 'b_questions', 'reach']

// Modelos con a lo más una pregunta por observable: sin numeración de
// lista y sin alta cuando ya existe la única.
const SINGLE_QUESTION_TYPES = ['reach', 'b_questions', 'special']

const FAMILIES = {
  a_questions: {
    snake: 'a_question', nested: 'a_questions',
    count: 'a_questions_count'},
  reach: {
    snake: 'reach_question', nested: 'reach_questions',
    count: 'reach_questions_count'},
  b_questions: {
    snake: 'b_question', nested: 'b_questions',
    count: 'b_questions_count'},
  plans: {
    snake: 'plan_question', nested: 'plan_questions',
    count: 'plan_questions_count'},
  special: {
    snake: 'special_question', nested: 'special_questions',
    count: 'special_questions_count'},
}

const DEFINITION_MESSAGE = 'Se guardó la definición del observable'
const CLOSED_BANNER = 'Cuestionario cerrado a edición. Puedes corregir '
  + 'textos y ponderaciones; no se agregan ni se eliminan preguntas ni tipos.'
const NO_TRIO_REASON = 'Este observable no usa el trío estándar '
  + '(armonización + sectorial + orgánica), así que ninguna ponderación se '
  + 'hereda del tipo: hay que capturarlas una por una.'
const NO_DEFAULT_REASON = 'Estos tipos no tienen ponderación por defecto '
  + 'en el catálogo, así que hay que capturarla aquí.'
const POPULATION_ALERT = 'Este tipo no tiene preguntas: la distribución de '
  + 'población se captura en «Información de base».'
const POPULATION_HINT =
  'Sin preguntas: se captura en «Información de base»'
const REQUIRED_EMPTY = 'Este tipo aplica al observable pero no tiene ninguna '
  + 'pregunta. Es un tipo requerido: el observable no se puede calificar así.'
const OPTIONAL_EMPTY = 'Este tipo todavía no tiene preguntas. Agrega la '
  + 'primera para que empiece a contar.'
const REQUIRED_TYPE_HINT = 'Requerido: siempre aplica'
const SAVE_TOOLTIP = 'Ctrl / Cmd + Enter dentro del texto guarda estos campos'
const REMOVE_TYPE_BODY = 'El observable dejará de calificarse en este tipo. '
  + 'Se puede volver a agregar mientras el cuestionario esté abierto.'
const ADD_TYPE_BODY = 'El observable pasará a calificarse también en este '
  + 'tipo. Se puede quitar mientras el cuestionario esté abierto.'
const DELETE_QUESTION_BODY =
  'Las respuestas ya capturadas de esta pregunta se borran con ella.'
const DELETE_WORD_HINT = 'Escribe «eliminar» para confirmar'
// `text` no admite vacío en ninguna de las cinco familias, así que el
// alta nace con un marcador que el foco deja seleccionado para escribir
// encima.
const NEW_QUESTION_TEXT = 'Nueva pregunta'
const ADD_QUESTION_ERROR = 'No se pudo agregar la pregunta.'
const DELETE_QUESTION_ERROR = 'No se pudo eliminar la pregunta.'
const ADD_TYPE_ERROR = 'No se pudo agregar el tipo de pregunta.'
const REMOVE_TYPE_ERROR = 'No se pudo quitar el tipo de pregunta.'

const full_main = defineModel({type: Object, required: true})

const emits = defineEmits(['item-saved'])

const { cats, schemas } = storeToRefs(useMainStore())
const { types_by_name } = useQuestionTypes()
const { showSnackbar } = useDashboardStore()
const theme = useTheme()

const saving = ref(false)
const errors = ref(null)
const creating = ref({})
const block_refs = ref({})
// Línea base de las ponderaciones: el `v-model` escribe sobre la propia
// fila puente, así que sin copia no hay forma de saber cuáles cambiaron.
const saved_weights = ref({})
const delete_dialog = ref({open: false, block: null, question: null,
  loading: false, text: '', warn: false})
const type_dialog = ref(
  {open: false, type: null, adding: false, loading: false})

const collection_data = computed(
  () => schemas.value.collections_dict.observable)

const bridge_collection = computed(
  () => schemas.value.collections_dict.observable_question_type)

// El store muta `cats` en sitio al guardar una categoría: el editor se
// reconfigura en vivo cuando alguien cierra el cuestionario.
const content_open = computed(
  () => cats.value?.questionnaire_settings?.[0]?.content_open ?? true)

const ordered_types = computed(
  () => [...(cats.value?.question_type || [])].sort(
    (a, b) => a.order - b.order))

const main_sectors_count = computed(
  () => (cats.value?.sector || []).filter(row => row.is_main).length)

const applied_rows = computed(() => {
  const rows = full_main.value.observable_question_types || []
  return [...rows].sort((a, b) =>
    (types_by_name.value[a.question_type]?.order || 0)
    - (types_by_name.value[b.question_type]?.order || 0))
})

const applied_names = computed(
  () => new Set(applied_rows.value.map(row => row.question_type)))

const rows_by_type = computed(() => Object.fromEntries(
  applied_rows.value.map(row => [row.question_type, row])))

// Las banderas del servidor quedan stale en cuanto se guarda un peso o
// se marca un tipo: todo el editor lee este cálculo, nunca el detalle.
const uses_default = computed(() => applied_names.value.size
  === STANDARD_TYPES.length
  && STANDARD_TYPES.every(name => applied_names.value.has(name)))

function isBlank(value) {
  return value === null || value === undefined || value === ''
}

function hasOwnWeight(row) {
  return !isBlank(row.weight)
}

function sameWeight(one, other) {
  if (isBlank(one) || isBlank(other))
    return isBlank(one) && isBlank(other)
  return Number(one) === Number(other)
}

function typeDefault(type_name) {
  return types_by_name.value[type_name]?.default_weight ?? null
}

function effectiveWeight(row) {
  if (hasOwnWeight(row))
    return row.weight
  return uses_default.value ? typeDefault(row.question_type) : null
}

const missing_blocks = computed(() => applied_rows.value
  .filter(row => effectiveWeight(row) === null)
  .map(row => types_by_name.value[row.question_type]?.public_name
    || row.question_type))

const weights_pending = computed(() => missing_blocks.value.length > 0)

const pending_text = computed(() => {
  const reason = uses_default.value ? NO_DEFAULT_REASON : NO_TRIO_REASON
  return `${reason} Faltan: ${joinNames(missing_blocks.value)}.`
})

const changed_weights = computed(() => applied_rows.value.filter(
  row => !sameWeight(row.weight, saved_weights.value[row.id])))

watch(applied_rows, rows => {
  rows.forEach(row => {
    if (!(row.id in saved_weights.value))
      saved_weights.value[row.id] = row.weight
  })
}, {immediate: true})

function joinNames(names) {
  if (names.length < 2)
    return names[0] || ''
  return `${names.slice(0, -1).join(', ')} y ${names[names.length - 1]}`
}

function questionsOf(type_name) {
  const family = FAMILIES[type_name]
  return family ? (full_main.value[family.nested] || []) : []
}

function formatWeight(value) {
  return isBlank(value) ? '' : String(Number(value))
}

// `QuestionType.color` es texto libre editable desde el dashboard: si no
// resuelve, el bloque se queda sin borde de color en vez de romperse.
function cssColor(name) {
  if (!name)
    return null
  const themed = theme.current.value.colors[name]
  if (themed)
    return themed
  const key = name.replace(/-(\w)/g, (_, letter) => letter.toUpperCase())
  return colors[key]?.base || null
}

function blockSubtitle(type, questions, sectors_count) {
  const parts = []
  if (type.name === 'reach' && questions.length)
    parts.push(`${sectors_count} ${
      sectors_count === 1 ? 'población' : 'poblaciones'}`)
  else if (FAMILIES[type.name] && questions.length)
    parts.push(`${questions.length} ${
      questions.length === 1 ? 'pregunta' : 'preguntas'}`)
  if (type.required)
    parts.push('Requerido')
  if (FAMILIES[type.name] && !questions.length)
    parts.push('sin preguntas')
  return parts.join(' · ')
}

function emptyAlert(type, questions) {
  if (!FAMILIES[type.name])
    return {type: 'info', text: POPULATION_ALERT}
  if (questions.length)
    return null
  return type.required
    ? {type: 'warning', text: REQUIRED_EMPTY}
    : {type: 'info', text: OPTIONAL_EMPTY}
}

function weightHint(row, type) {
  const type_default = typeDefault(type.name)
  if (hasOwnWeight(row))
    return type_default === null
      ? 'Propia del observable (el tipo no trae default)'
      : `Propia del observable (el tipo usa ${formatWeight(type_default)})`
  if (uses_default.value && type_default !== null)
    return `Sin valor propio: usa ${formatWeight(type_default)} del tipo`
  return 'Falta capturar'
}

function reachSectorsCount() {
  const reach = questionsOf('reach')[0]
  if (!reach)
    return 0
  return (reach.others_sectors || []).length
    + (reach.has_main_sectors ? main_sectors_count.value : 0)
}

function typeState(type) {
  const checked = applied_names.value.has(type.name)
  const count = questionsOf(type.name).length
  if (type.required)
    return {checked, readonly: true, disabled: false,
      hint: REQUIRED_TYPE_HINT}
  if (!content_open.value)
    return {checked, readonly: true, disabled: false, hint: ''}
  if (checked && count)
    return {checked, readonly: false, disabled: true,
      hint: count === 1
        ? 'Elimina antes su pregunta'
        : `Elimina antes sus ${count} preguntas`}
  return {checked, readonly: false, disabled: false,
    hint: !checked && !FAMILIES[type.name] ? POPULATION_HINT : ''}
}

// Una fila por tipo del catálogo: la casilla que decide si aplica y, si
// aplica, la ponderación de este observable para ese tipo.
const type_list = computed(() => ordered_types.value.map(type => {
  const row = rows_by_type.value[type.name] || null
  return {
    type,
    row,
    ...typeState(type),
    weight_hint: row ? weightHint(row, type) : '',
    weight_placeholder: row && !hasOwnWeight(row) && uses_default.value
      ? formatWeight(typeDefault(type.name)) : '',
    weight_missing: row ? effectiveWeight(row) === null : false,
  }
}))

const blocks = computed(() => applied_rows.value.reduce((acc, row) => {
  const type = types_by_name.value[row.question_type]
  if (!type)
    return acc
  const questions = questionsOf(type.name)
  const alert = emptyAlert(type, questions)
  const single = SINGLE_QUESTION_TYPES.includes(type.name)
  acc.push({
    row,
    type,
    questions,
    single,
    family: FAMILIES[type.name] || null,
    subtitle: blockSubtitle(type, questions, reachSectorsCount()),
    empty_alert: alert,
    // Las familias de una sola pregunta arman un grupo alto (texto más
    // controles propios): sus acciones van debajo, no en una columna.
    actions_below: ['reach', 'b_questions'].includes(type.name),
    show_add: !!FAMILIES[type.name] && (!single || !questions.length),
    list_subtitle: ['a_questions', 'special'].includes(type.name),
    // El bloque requerido y vacío cambia el borde a warning: es la única
    // condición que compite con la identidad de color del tipo.
    border_color: cssColor(
      alert?.type === 'warning' ? 'warning' : type.color),
    save_message: ['reach', 'b_questions'].includes(type.name)
      ? `Se guardó la pregunta de ${type.public_name}`
      : undefined,
  })
  return acc
}, []))

const row_sync = computed(() => {
  const b_question = questionsOf('b_questions')[0] || {}
  const sync = {
    id: full_main.value.id,
    weights_pending: weights_pending.value,
    uses_default_weights: uses_default.value,
    question_types: applied_rows.value.map(row => row.question_type),
    reach_sectors_count: reachSectorsCount(),
    b_includes_academic: !!b_question.includes_academic,
    b_includes_admin: !!b_question.includes_admin,
  }
  Object.values(FAMILIES).forEach(family => {
    sync[family.count] = (full_main.value[family.nested] || []).length
  })
  return sync
})

function emitRowSync() {
  emits('item-saved', {res: row_sync.value, is_new: false})
}

// Un solo botón para los textos del observable y para las ponderaciones
// que cambiaron: son dos recursos, pero una sola decisión del usuario.
async function saveDefinition() {
  errors.value = null
  saving.value = true
  const failed = []
  for (const row of changed_weights.value) {
    const weight = hasOwnWeight(row) ? row.weight : null
    const res = await patchElement(bridge_collection.value, row.id, {weight})
    if (res.errors) {
      failed.push(types_by_name.value[row.question_type]?.public_name
        || row.question_type)
      continue
    }
    Object.assign(row, res.data)
    saved_weights.value[row.id] = res.data.weight
  }
  const res = await saveElement(collection_data.value, full_main.value)
  saving.value = false
  if (res.errors) {
    errors.value = res.errors
    return
  }
  emits('item-saved', {res: {...res.data, ...row_sync.value}, is_new: false})
  if (failed.length)
    showSnackbar(`Error: no se guardó la ponderación de ${joinNames(failed)}`)
  else
    showSnackbar(DEFINITION_MESSAGE)
}

async function addQuestion(block) {
  const type_name = block.type.name
  creating.value[type_name] = true
  const collection = schemas.value.collections_dict[block.family.snake]
  const res = await saveElement(
    collection, {observable: full_main.value.id, text: NEW_QUESTION_TEXT},
    ADD_QUESTION_ERROR)
  creating.value[type_name] = false
  if (res.errors)
    return
  block.questions.push(res.data)
  emitRowSync()
  showSnackbar('Se agregó una pregunta')
  await nextTick()
  const areas = block_refs.value[type_name]?.querySelectorAll('textarea')
  areas?.[areas.length - 1]?.select()
}

function askDeleteQuestion(block, question) {
  delete_dialog.value = {
    open: true, block, question, loading: false, text: '', warn: false}
}

async function deleteQuestion() {
  const dialog = delete_dialog.value
  // El aviso va dentro del diálogo: un snackbar quedaría bajo el overlay.
  dialog.warn = dialog.text?.trim().toLowerCase() !== 'eliminar'
  if (dialog.warn)
    return
  dialog.loading = true
  const collection = schemas.value.collections_dict[dialog.block.family.snake]
  const res = await deleteElement(
    collection, dialog.question.id, DELETE_QUESTION_ERROR)
  dialog.loading = false
  if (res.errors)
    return
  const list = dialog.block.questions
  list.splice(list.indexOf(dialog.question), 1)
  dialog.open = false
  emitRowSync()
  showSnackbar('Se eliminó la pregunta')
}

function toggleType(type, checked) {
  type_dialog.value = {open: true, type, adding: checked, loading: false}
}

function confirmTypeChange() {
  return type_dialog.value.adding ? addType() : removeType()
}

async function addType() {
  const dialog = type_dialog.value
  dialog.loading = true
  const res = await saveElement(
    bridge_collection.value,
    {observable: full_main.value.id, question_type: dialog.type.name},
    ADD_TYPE_ERROR)
  dialog.loading = false
  if (res.errors)
    return
  full_main.value.observable_question_types.push(res.data)
  dialog.open = false
  emitRowSync()
  showSnackbar(`Se agregó ${dialog.type.public_name}`)
  await nextTick()
  block_refs.value[dialog.type.name]
    ?.querySelector('.add-question button')?.focus()
}

async function removeType() {
  const dialog = type_dialog.value
  const rows = full_main.value.observable_question_types
  const row = rows.find(item => item.question_type === dialog.type.name)
  if (!row) {
    dialog.open = false
    return
  }
  dialog.loading = true
  const res = await deleteElement(
    bridge_collection.value, row.id, REMOVE_TYPE_ERROR)
  dialog.loading = false
  if (res.errors)
    return
  rows.splice(rows.indexOf(row), 1)
  dialog.open = false
  emitRowSync()
  showSnackbar(`Se quitó ${dialog.type.public_name}`)
}

function onQuestionSaved(block, {res}) {
  const index = block.questions.findIndex(item => item.id === res.id)
  if (index !== -1)
    block.questions[index] = res
  emitRowSync()
}

</script>

<template>
  <v-card class="mb-3 pa-3" elevation="8">
    <v-alert
      v-if="errors"
      type="error"
      class="mb-3"
      style="white-space: pre-wrap;"
    >
      {{ errors }}
    </v-alert>

    <v-alert
      v-if="!content_open"
      type="info"
      variant="tonal"
      density="compact"
      border="start"
      icon="lock"
      class="mb-3"
    >
      {{ CLOSED_BANNER }}
    </v-alert>

    <v-card variant="outlined" class="mb-4 pa-3">
      <h3 class="text-subtitle-1 font-weight-bold mb-3">
        <v-icon class="mr-2">assignment</v-icon>
        Definición del observable
      </h3>
      <div class="d-flex flex-wrap ga-3">
        <v-text-field
          :model-value="full_main.number"
          label="Número"
          readonly
          persistent-hint
          variant="outlined"
          density="comfortable"
          style="max-width: 110px;"
        />
        <v-text-field
          v-model="full_main.name"
          label="Nombre del observable"
          variant="outlined"
          density="comfortable"
          style="flex: 1 1 320px;"
        />
      </div>
      <v-textarea
        v-model="full_main.description"
        label="Descripción"
        variant="outlined"
        density="comfortable"
        rows="1"
        auto-grow
        class="reading-width mt-3"
        @keydown.ctrl.enter.prevent="saveDefinition"
        @keydown.meta.enter.prevent="saveDefinition"
      />
      <v-textarea
        v-model="full_main.init_question"
        label="Pregunta inicial (sí / no)"
        hint="La que abre el observable y decide si se captura lo demás"
        persistent-hint
        variant="outlined"
        density="comfortable"
        rows="2"
        auto-grow
        class="reading-width mt-3"
        @keydown.ctrl.enter.prevent="saveDefinition"
        @keydown.meta.enter.prevent="saveDefinition"
      />

      <v-divider class="my-3 dotted"></v-divider>
      <h4 class="text-subtitle-2 font-weight-bold mb-2">
        Tipos de pregunta que aplican
      </h4>

      <v-alert
        v-if="weights_pending"
        type="warning"
        variant="tonal"
        density="compact"
        aria-live="polite"
        class="mb-3"
      >
        <div class="font-weight-bold">Ponderación pendiente</div>
        {{ pending_text }}
      </v-alert>

      <div
        v-for="entry in type_list"
        :key="entry.type.name"
        class="d-flex align-start flex-wrap ga-3 type-row"
      >
        <div class="pt-1" style="flex: 0 1 340px;">
          <v-checkbox
            :model-value="entry.checked"
            :readonly="entry.readonly"
            :disabled="entry.disabled"
            density="compact"
            hide-details
            @update:model-value="value => toggleType(entry.type, value)"
          >
            <template #label>
              <v-icon :color="entry.type.color" class="mr-2">
                {{ entry.type.icon }}
              </v-icon>
              {{ entry.type.public_name }}
            </template>
          </v-checkbox>
          <div
            v-if="entry.hint"
            class="text-caption text-medium-emphasis ml-10"
          >
            {{ entry.hint }}
          </div>
        </div>
        <!-- El hint va fuera del campo: `.v-input__details` no crece
             cuando el texto ocupa dos renglones y se montaba sobre la
             fila siguiente. `aria-describedby` conserva el enlace. -->
        <div v-if="entry.row" style="flex: 0 0 200px;">
          <v-text-field
            v-model="entry.row.weight"
            label="Ponderación"
            type="number"
            step="0.5"
            min="0"
            clearable
            hide-details
            :placeholder="entry.weight_placeholder"
            persistent-placeholder
            :aria-describedby="`weight-hint-${entry.type.name}`"
            :base-color="entry.weight_missing ? 'warning' : undefined"
            :color="entry.weight_missing ? 'warning' : undefined"
            variant="outlined"
            density="compact"
          />
          <div
            :id="`weight-hint-${entry.type.name}`"
            class="text-caption mt-1"
            :class="entry.weight_missing
              ? 'text-warning' : 'text-medium-emphasis'"
          >
            {{ entry.weight_hint }}
          </div>
        </div>
      </div>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="accent"
          variant="elevated"
          :loading="saving"
          @click="saveDefinition"
        >
          Guardar
          <v-tooltip activator="parent" location="top">
            {{ SAVE_TOOLTIP }}
          </v-tooltip>
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-card
      v-for="block in blocks"
      :key="block.row.id"
      class="mb-4 pa-3 border-s-lg type-block"
      elevation="4"
      :style="{'--block-color': block.border_color}"
    >
      <h3 class="text-subtitle-1 font-weight-bold">
        <v-icon :color="block.type.color" class="mr-2">
          {{ block.type.icon }}
        </v-icon>
        {{ block.type.public_name }}
      </h3>
      <div class="text-caption text-medium-emphasis mb-3">
        {{ block.subtitle }}
      </div>

      <template v-if="block.type.name === 'a_questions'">
        <v-textarea
          v-model="full_main.a_main_question"
          label="Enunciado del bloque"
          variant="outlined"
          density="comfortable"
          rows="2"
          auto-grow
          class="reading-width"
          @keydown.ctrl.enter.prevent="saveDefinition"
          @keydown.meta.enter.prevent="saveDefinition"
        />
        <v-textarea
          v-model="full_main.a_main_subtitle"
          label="Instrucción para quien responde"
          variant="outlined"
          density="comfortable"
          rows="1"
          auto-grow
          class="reading-width"
          @keydown.ctrl.enter.prevent="saveDefinition"
          @keydown.meta.enter.prevent="saveDefinition"
        />
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="accent"
            variant="elevated"
            :loading="saving"
            @click="saveDefinition"
          >
            Guardar
            <v-tooltip activator="parent" location="top">
              {{ SAVE_TOOLTIP }}
            </v-tooltip>
          </v-btn>
        </v-card-actions>
        <v-divider class="mb-3 dotted"></v-divider>
      </template>

      <v-alert
        v-if="block.empty_alert"
        :type="block.empty_alert.type"
        variant="tonal"
        density="compact"
        class="mb-3"
      >
        {{ block.empty_alert.text }}
      </v-alert>

      <div :ref="el => block_refs[block.type.name] = el">
        <div
          v-if="block.list_subtitle && block.questions.length"
          class="text-subtitle-2 font-weight-bold"
        >
          Preguntas:
        </div>
        <template
          v-for="(question, index) in block.questions"
          :key="question.id"
        >
          <v-divider v-if="index"></v-divider>
          <ObservableQuestionEdit
            :model-value="question"
            :collection_snake="block.family.snake"
            text_label="Texto de la pregunta"
            :position="block.single ? null : index + 1"
            :success_message="block.save_message"
            :actions_below="block.actions_below"
            in_block
            @item-saved="onQuestionSaved(block, $event)"
          >
            <template
              v-if="block.type.name === 'b_questions'"
              #before
            >
              <OrgInstancesFields
                :model-value="question"
                :readonly="!content_open"
              />
            </template>
            <template
              v-if="block.type.name === 'reach'"
              #after
            >
              <ReachSectorFields
                :model-value="question"
                :readonly="!content_open"
              />
            </template>
            <template
              v-if="content_open"
              #actions
            >
              <v-btn
                icon="delete"
                variant="text"
                color="error"
                size="small"
                aria-label="Eliminar esta pregunta"
                @click="askDeleteQuestion(block, question)"
              />
            </template>
          </ObservableQuestionEdit>
        </template>
        <div
          v-if="content_open && block.show_add"
          class="d-flex justify-center add-question"
        >
          <v-btn
            variant="tonal"
            prepend-icon="add"
            :loading="creating[block.type.name]"
            @click="addQuestion(block)"
          >
            Agregar pregunta
          </v-btn>
        </div>
      </div>
    </v-card>

    <DialogDelete
      v-model="delete_dialog.open"
      v-model:delete_text="delete_dialog.text"
      is_saved
      title="¿Eliminar esta pregunta?"
      :loading="delete_dialog.loading"
      @confirm-delete="deleteQuestion"
    >
      {{ DELETE_QUESTION_BODY }}
      <div v-if="delete_dialog.warn" class="text-caption text-warning">
        {{ DELETE_WORD_HINT }}
      </div>
    </DialogDelete>

    <ConfirmActionDialog
      v-model="type_dialog.open"
      :title="type_dialog.adding
        ? `¿Agregar ${type_dialog.type?.public_name} a este observable?`
        : `¿Quitar ${type_dialog.type?.public_name} de este observable?`"
      :confirm-label="type_dialog.adding ? 'Agregar' : 'Quitar'"
      :confirm-icon="type_dialog.adding ? 'add' : 'delete'"
      :loading="type_dialog.loading"
      @confirm="confirmTypeChange"
    >
      {{ type_dialog.adding ? ADD_TYPE_BODY : REMOVE_TYPE_BODY }}
    </ConfirmActionDialog>
  </v-card>
</template>

<style scoped>
/* Tope de ancho de lectura para el cotejo de textos; el panel del
   dashboard es mucho más ancho. */
.reading-width {
  max-width: 90ch;
}

/* `border-s-lg` fija el color con !important; la variable es la única
   forma de que el borde lleve el color del tipo. */
.type-block.border-s-lg {
  border-inline-start-color: var(--block-color) !important;
}

.dotted {
  border-style: dotted;
}

.type-row {
  min-height: 72px;
}
</style>
