<script setup>
/**
 * Grupo `autoridades`: quién encabeza la institución y cómo se compone su
 * alto mando.
 *
 * Las autoridades no declaran presencia (no son poblaciones objetivo): solo
 * generan filas de PopulationQuantity, sin el tri-estado de poblaciones. Su
 * escape es el opt-out «No aplica» por renglón (`no_apply`, task-56), para
 * el cuerpo que una IES pueda no tener.
 *
 * La titular es unipersonal: se pregunta por su sexo y género con un radio y
 * se persiste como una fila de total 1 (el conteo que corresponde en 1 y los
 * otros en 0). Esa cocina no se muestra nunca en la interfaz.
 */
import GeneralCountCells from
  '~/components/dashboard/survey/GeneralCountCells.vue'
import { useGeneralSurvey } from '~/composables/useGeneralSurvey.js'

defineProps({
  // Solo se leen los textos: las filas de este grupo salen del catálogo
  // Sector, no de `questions`.
  catalog: { type: Object, default: () => ({}) },
  editable: { type: Boolean, default: false },
  // Claves de los campos que la compuerta de completado marcó como
  // faltantes (useGeneralValidation).
  invalid: { type: Set, default: () => new Set() },
})

const survey = defineModel({ type: Object, required: true })

const { iesHead, authorityBodies, rowFor, ensureRows, clearCounts, rowTotal } =
  useGeneralSurvey(survey)

// La tabla lee `rowFor(...)` directo en los v-model: las filas deben existir
// antes de pintar (idempotente, el padre ya lo hizo al cargar).
watch(survey, ensureRows, { immediate: true })

// Una sola bandera para las dos tablas: es capacidad de medición de la
// institución, no propiedad de cada tabla (task-110).
const showNonBinary = computed(() => survey.value?.measures_non_binary === true)

const headSex = computed({
  get() {
    const row = iesHead.value ? rowFor(iesHead.value.id) : null
    if (!row) return null
    if (row.number_women === 1) return 'women'
    if (row.number_men === 1) return 'men'
    if (row.number_non_binary === 1) return 'non_binary'
    return null
  },
  set(value) {
    const row = iesHead.value ? rowFor(iesHead.value.id) : null
    if (!row) return
    row.number_women = value === 'women' ? 1 : 0
    row.number_men = value === 'men' ? 1 : 0
    row.number_non_binary = value === 'non_binary' ? 1 : 0
  },
})

const isCountable = (sector) => rowFor(sector.id)?.no_apply !== true

const onNoApplyChange = (sector) => {
  if (!isCountable(sector)) clearCounts(sector.id)
}
</script>

<template>
  <div>
    <div v-if="iesHead" class="mb-6">
      <div class="text-body-1 font-weight-medium mb-1">
        La persona titular de la institución es:
      </div>
      <v-radio-group
        v-model="headSex"
        :readonly="!editable"
        :error="invalid.has('head')"
        inline
        hide-details="auto"
      >
        <v-radio label="Mujer" value="women" color="accent" />
        <v-radio label="Hombre" value="men" color="accent" />
        <v-radio
          v-if="showNonBinary"
          label="No binaria"
          value="non_binary"
          color="accent"
        />
      </v-radio-group>
    </div>

    <!-- La instrucción del grupo describe esta tabla, no el radio de la
         titular: por eso la coloca el hijo y el panel la omite
         (OWN_INSTRUCTION_GROUPS en GeneralGroupPanel). -->
    <p
      v-if="catalog.instruction"
      class="text-body-1 text-grey-darken-1 mb-4"
    >
      {{ catalog.instruction }}
    </p>

    <v-defaults-provider
      :defaults="{ VCountInput: { density: 'compact', hideDetails: true } }"
    >
    <v-table density="comfortable" class="border rounded">
      <thead>
        <tr>
          <th class="text-left text-body-1">Autoridad</th>
          <th class="text-center text-body-1" style="width: 150px">Mujeres</th>
          <th class="text-center text-body-1" style="width: 150px">Hombres</th>
          <th
            v-if="showNonBinary"
            class="text-center text-body-1"
            style="width: 150px"
          >
            No binarie
          </th>
          <th class="text-right text-body-1" style="width: 150px">Total</th>
          <th class="text-center text-body-1" style="width: 110px">
            No aplica
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="sector in authorityBodies"
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
          </td>
          <GeneralCountCells
            :row="rowFor(sector.id)"
            :sector="sector"
            :editable="editable"
            :disabled="!isCountable(sector)"
            :show-non-binary="showNonBinary"
            :invalid="invalid"
            :total="rowTotal(sector.id)"
          />
          <td class="text-center">
            <v-checkbox
              v-model="rowFor(sector.id).no_apply"
              :readonly="!editable"
              :aria-label="`No aplica — ${sector.name}`"
              color="accent"
              density="compact"
              hide-details
              class="d-inline-flex"
              @update:model-value="onNoApplyChange(sector)"
            />
          </td>
        </tr>
      </tbody>
    </v-table>
    </v-defaults-provider>
  </div>
</template>
