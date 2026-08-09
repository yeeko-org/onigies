<script setup>
/**
 * Grupo `autoridades`: quién encabeza la institución y cómo se compone su
 * alto mando.
 *
 * Las autoridades NO se agregan a `Survey.sectors` (no son poblaciones
 * objetivo): solo generan filas de PopulationQuantity, y las tres colegiadas
 * existen siempre, así que la tabla no lleva columna «Existe».
 *
 * La titular es unipersonal: se pregunta por su sexo con un radio y se
 * persiste como una fila de total 1 (`number_women` 0/1 y `number_men` el
 * complemento). Esa cocina no se muestra nunca en la interfaz.
 */
import { useGeneralSurvey } from '~/composables/useGeneralSurvey.js'

defineProps({
  editable: { type: Boolean, default: false },
})

const survey = defineModel({ type: Object, required: true })

const { iesHead, authorityBodies, rowFor, ensureRows, rowTotal } =
  useGeneralSurvey(survey)

// La tabla lee `rowFor(...)` directo en los v-model: las filas deben existir
// antes de pintar (idempotente, el padre ya lo hizo al cargar).
watch(survey, ensureRows, { immediate: true })

const headSex = computed({
  get() {
    const row = iesHead.value ? rowFor(iesHead.value.id) : null
    if (!row) return null
    if (row.number_women === 1) return 'women'
    if (row.number_men === 1) return 'men'
    return null
  },
  set(value) {
    const row = iesHead.value ? rowFor(iesHead.value.id) : null
    if (!row) return
    row.number_women = value === 'women' ? 1 : 0
    row.number_men = value === 'men' ? 1 : 0
  },
})
</script>

<template>
  <div>
    <div v-if="iesHead" class="mb-6">
      <div class="text-body-2 font-weight-medium mb-1">
        La persona titular de la institución es:
      </div>
      <v-radio-group
        v-model="headSex"
        :readonly="!editable"
        inline
        hide-details="auto"
      >
        <v-radio label="Mujer" value="women" color="accent" />
        <v-radio label="Hombre" value="men" color="accent" />
      </v-radio-group>
    </div>

    <p class="text-body-2 mb-4">
      Indique cuántas personas integran, según su sexo, cada uno de los
      siguientes órganos y conjuntos de autoridades de su institución.
    </p>

    <v-defaults-provider
      :defaults="{ VCountInput: { density: 'compact', hideDetails: true } }"
    >
    <v-table density="comfortable" class="border rounded">
      <thead>
        <tr>
          <th class="text-left">Autoridad</th>
          <th class="text-right" style="width: 150px">Hombres</th>
          <th class="text-right" style="width: 150px">Mujeres</th>
          <th class="text-right" style="width: 110px">Total</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="sector in authorityBodies"
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
          </td>
          <td>
            <v-count-input
              v-model="rowFor(sector.id).number_men"
              :readonly="!editable"
              :aria-label="`Hombres — ${sector.name}`"
              inputmode="numeric"
            />
          </td>
          <td>
            <v-count-input
              v-model="rowFor(sector.id).number_women"
              :readonly="!editable"
              :aria-label="`Mujeres — ${sector.name}`"
              inputmode="numeric"
            />
          </td>
          <td class="text-right text-body-2 font-weight-medium">
            {{ rowTotal(sector.id) ?? '—' }}
          </td>
        </tr>
      </tbody>
    </v-table>
    </v-defaults-provider>
  </div>
</template>
