<script setup>
/**
 * Grupo `poblaciones`: una sola tabla con las ~12 poblaciones del catálogo
 * (los 10 sectores principales más los 2 extra de POB-ESTÁNDAR).
 *
 * Dos respuestas distintas conviven en cada renglón: «Se atiende» es la
 * pertenencia a `Survey.sectors` (M2M) y los conteos son una fila de
 * PopulationQuantity. Los 2 sectores extra solo se marcan: son poblaciones
 * estructurales (población externa y público en general) de las que la IES no
 * lleva registro nominal, así que nunca llevan conteo.
 */
 import { useGeneralSurvey } from '~/composables/useGeneralSurvey.js'

const props = defineProps({
  editable: { type: Boolean, default: false },
})

const survey = defineModel({ type: Object, required: true })

const { populationSectors, rowFor, ensureRows, isSelected, rowTotal } =
  useGeneralSurvey(survey)

// La tabla lee `rowFor(...)` directo en los v-model, así que las filas deben
// existir antes de pintar; es idempotente y barato repetirlo aquí aunque el
// padre ya lo haya hecho al cargar.
watch(survey, ensureRows, { immediate: true })

// Los conteos se deshabilitan (no se ocultan) hasta marcar «Se atiende»
const canCount = (sector) =>
    props.editable && sector.is_main && isSelected(sector.id)

</script>

<template>
  <div>
    <p class="text-body-2 mb-1">
      Señale las poblaciones que integran a la comunidad de su institución,
      así como todas aquellas que están presentes física o virtualmente y con
      las que mantiene vínculos a través de sus actividades institucionales.
    </p>
    <p class="text-body-2 text-grey-darken-1 mb-4">
      Para cada población marcada, indique cuántas personas la integran según
      su sexo. Si no cuenta con el dato exacto, registre su mejor estimación.
    </p>

    <v-defaults-provider
      :defaults="{ VCountInput: { density: 'compact', hideDetails: true } }"
    >
      <v-table density="comfortable" class="border rounded">
        <thead>
          <tr>
            <th class="text-left">Población</th>
            <th class="text-center" style="width: 102px">Se atiende</th>
            <th class="text-center" style="width: 150px">Mujeres</th>
            <th class="text-center" style="width: 150px">Hombres</th>
            <th class="text-center" style="width: 150px">No binarie</th>
            <th class="text-right" style="width: 110px">Total</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="sector in populationSectors"
            :key="sector.id"
          >
            <td class="py-2">
              <div class="text-body-2 font-weight-medium">
                {{ sector.name }}
              </div>
              <div
                v-if="sector.description"
                class="text-caption text-grey-darken-1"
              >
                {{ sector.description }}
              </div>
              <v-text-field
                v-if="sector.needs_name && isSelected(sector.id)"
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
              <v-checkbox
                v-model="survey.sectors"
                :value="sector.id"
                :readonly="!editable"
                color="accent"
                density="compact"
                hide-details
                class="d-inline-flex"
              />
            </td>
            <!-- Sectores estructurales: existen o no, nunca se cuentan. -->
            <template v-if="!sector.is_main">
              <td class="text-center text-disabled" colspan="3">
                No requiere conteo
              </td>
            </template>
            <template v-else>
              <td>
                <v-count-input
                  v-model="rowFor(sector.id).number_women"
                  :disabled="!canCount(sector)"
                  :aria-label="`Mujeres — ${sector.name}`"
                  inputmode="numeric"
                />
              </td>
              <td>
                <v-count-input
                  v-model="rowFor(sector.id).number_men"
                  :disabled="!canCount(sector)"
                  :aria-label="`Hombres — ${sector.name}`"
                  type="number"
                />
              </td>
              <td>
                <v-count-input
                  v-model="rowFor(sector.id).no_binarie"
                  :disabled="!canCount(sector)"
                  :aria-label="`Hombres — ${sector.name}`"
                  type="number"
                />
              </td>
              <td class="text-right text-body-2 font-weight-medium">
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
