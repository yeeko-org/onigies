<script setup>
/**
 * Grupo `poblaciones`: una sola tabla con las ~12 poblaciones del catálogo
 * (los 10 sectores principales más los 2 extra de POB-ESTÁNDAR).
 *
 * Dos respuestas distintas conviven en cada renglón, y las dos viven en la
 * misma fila de PopulationQuantity: «Está presente» es el tri-estado
 * `is_present` (adr-0012) y los conteos son sus tres columnas. Los 2
 * sectores extra solo declaran presencia: son poblaciones estructurales
 * (población externa y público en general) de las que la IES no lleva
 * registro nominal, así que nunca llevan conteo.
 */
 import { useGeneralSurvey, questionByName } from
   '~/composables/useGeneralSurvey.js'

const props = defineProps({
  catalog: { type: Object, default: () => ({}) },
  editable: { type: Boolean, default: false },
  // Claves de los campos que la compuerta de completado marcó como
  // faltantes (useGeneralValidation); vacío mientras nadie intentó
  // completar el grupo.
  invalid: { type: Set, default: () => new Set() },
})

const survey = defineModel({ type: Object, required: true })

const { populationSectors, rowFor, ensureRows, isPresent, clearCounts,
  clearNonBinary, rowTotal } = useGeneralSurvey(survey)

// La tabla lee `rowFor(...)` directo en los v-model, así que las filas deben
// existir antes de pintar; es idempotente y barato repetirlo aquí aunque el
// padre ya lo haya hecho al cargar.
watch(survey, ensureRows, { immediate: true })

// Pregunta previa del grupo: es capacidad de medición de la institución,
// no propiedad de la tabla, por eso va antes y una sola vez.
const nonBinaryQuestion = computed(
  () => questionByName(props.catalog, 'measures_non_binary'))

// La columna no binaria se pinta solo si la institución declara que mide esa
// población: sin esa capacidad la columna pediría un dato inexistente.
const showNonBinary = computed(() => survey.value?.measures_non_binary === true)

// Solo «Sí» y «No»: el nulo es la fila que nadie tocó y no se ofrece.
const PRESENCE_OPTIONS = [
  { title: 'Sí', value: true },
  { title: 'No', value: false },
]

// Los conteos quedan deshabilitados (no ocultos) mientras la población no
// esté presente: la exclusión viene de una respuesta previa.
const isCountable = (sector) => sector.is_main && isPresent(sector.id)

const onPresenceChange = (sector) => {
  if (!isPresent(sector.id)) clearCounts(sector.id)
}

// Solo el «no» explícito limpia (mismo criterio que `is_present`): el
// nulo es «sin contestar» y no borra nada.
const onNonBinaryChange = (value) => {
  if (value === false) clearNonBinary()
}

const countError = (sector, field) =>
  props.invalid.has(`count:${sector.id}:${field}`)
</script>

<template>
  <div>
    <div v-if="nonBinaryQuestion" class="mb-4">
      <div class="text-body-1 font-weight-medium mb-1">
        {{ nonBinaryQuestion.text }}
      </div>
      <div
        v-if="nonBinaryQuestion.hint"
        class="text-caption text-grey-darken-1 mb-1"
      >
        {{ nonBinaryQuestion.hint }}
      </div>
      <v-radio-group
        v-model="survey.measures_non_binary"
        :readonly="!editable"
        :error="invalid.has('question:measures_non_binary')"
        inline
        hide-details="auto"
        @update:model-value="onNonBinaryChange"
      >
        <v-radio label="Sí" :value="true" color="accent" />
        <v-radio label="No" :value="false" color="accent" />
      </v-radio-group>
    </div>

    <v-defaults-provider
      :defaults="{ VCountInput: { density: 'compact', hideDetails: true } }"
    >
      <v-table density="comfortable" class="border rounded">
        <thead>
          <tr>
            <th class="text-left text-body-1">Población</th>
            <th class="text-center text-body-1" style="width: 130px">
              Está presente
            </th>
            <th class="text-right text-body-1" style="width: 150px">
              Mujeres
            </th>
            <th class="text-right text-body-1" style="width: 150px">
              Hombres
            </th>
            <th
              v-if="showNonBinary"
              class="text-right text-body-1"
              style="width: 150px"
            >
              No binarie
            </th>
            <th class="text-right text-body-1" style="width: 150px">Total</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="sector in populationSectors"
            :key="sector.id"
          >
            <td class="py-2">
              <div class="text-body-1 font-weight-medium">
                {{ sector.name }}
              </div>
              <div
                v-if="sector.description"
                class="text-caption text-grey-darken-1"
              >
                {{ sector.description }}
              </div>
              <v-text-field
                v-if="sector.needs_name && isPresent(sector.id)"
                v-model="rowFor(sector.id).name"
                label="¿Cómo se llama en su institución?"
                variant="outlined"
                density="compact"
                hide-details="auto"
                :readonly="!editable"
                class="mt-2"
                style="max-width: 420px"
              />
            </td>
            <td class="text-center">
              <v-select
                v-model="rowFor(sector.id).is_present"
                :items="PRESENCE_OPTIONS"
                :readonly="!editable"
                :error="invalid.has(`presence:${sector.id}`)"
                :aria-label="`Está presente — ${sector.name}`"
                variant="outlined"
                density="compact"
                hide-details
                @update:model-value="onPresenceChange(sector)"
              />
            </td>
            <!-- Sectores estructurales: están presentes o no, nunca se
                 cuentan. -->
            <template v-if="!sector.is_main">
              <td
                class="text-center text-disabled text-body-1"
                :colspan="showNonBinary ? 4 : 3"
              >
                No requiere conteo
              </td>
            </template>
            <template v-else>
              <td class="text-right">
                <v-count-input
                  v-model="rowFor(sector.id).number_women"
                  :readonly="!editable"
                  :disabled="!isCountable(sector)"
                  :error="countError(sector, 'number_women')"
                  :aria-label="`Mujeres — ${sector.name}`"
                  inputmode="numeric"
                />
              </td>
              <td class="text-right">
                <v-count-input
                  v-model="rowFor(sector.id).number_men"
                  :readonly="!editable"
                  :disabled="!isCountable(sector)"
                  :error="countError(sector, 'number_men')"
                  :aria-label="`Hombres — ${sector.name}`"
                  inputmode="numeric"
                />
              </td>
              <td v-if="showNonBinary" class="text-right">
                <v-count-input
                  v-model="rowFor(sector.id).number_non_binary"
                  :readonly="!editable"
                  :disabled="!isCountable(sector)"
                  :error="countError(sector, 'number_non_binary')"
                  :aria-label="`No binarie — ${sector.name}`"
                  inputmode="numeric"
                />
              </td>
              <td class="text-right text-body-1 font-weight-medium">
                {{ rowTotal(sector.id) ?? '—' }}
              </td>
            </template>
          </tr>
        </tbody>
      </v-table>
    </v-defaults-provider>
  </div>
</template>

<style scoped>
</style>
