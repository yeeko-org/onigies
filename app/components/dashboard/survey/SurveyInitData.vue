<script setup>
import {storeToRefs} from "pinia";
import {useIesStore} from "~/store/ies.js";
import {useMainStore} from '~/store/index.js'
const iesStore = useIesStore()
const mainStore = useMainStore()

const current_period = computed(() => iesStore.current_period)
const { all_months } = storeToRefs(iesStore)
const { cats } = storeToRefs(mainStore)
import {useRules} from "~/composables/useRules.js";
const { rules } = useRules()

const props = defineProps({
  period: { type: Number, required: false },
  survey_id: { type: Number, required: false },
})
const survey_data = ref(null)

const plan_types = [
  { key: "media_plans", name: "nivel medio superior" },
  // { key: "superior_plans", name: "nivel superior (licenciatura)" },
  // { key: "postgraduate_plans", name: "nivel posgrado (especialidad, maestría y doctorado)" },
  { key: "superior_plans", name: "nivel superior", description: "licenciatura" },
  { key: "postgraduate_plans", name: "nivel posgrado", description: "especialidad, maestría y doctorado" },
]

const main_sectors = computed(() => {
  console.log("cats", cats.value)
  if (!cats.value?.sector)
    return []
  return cats.value.sector.filter(sector => sector.is_main)
})

async function loadSurvey(survey_id) {
  survey_data.value = await mainStore.getSimple([ "survey", survey_id ])
}

watch(() => props.period, (newVal) => {
  if (newVal) {
    loadSurvey(props.survey_id)
  }
}, { immediate: true })

</script>

<template>
  <v-card v-if="survey_data" class="pa-3" elevation="6">
    <v-card-title class="text-h5 mb-4">
      Datos generales
    </v-card-title>
<!--    <v-alert type="info">-->
<!--      Esta sección está ahora en desarrollo,-->
<!--      sólo está disponible la sección de Buenas Prácticas.-->
<!--    </v-alert>-->
    <v-card
      variant="outlined"
    >
      <v-card-title class="text-secondary">
        Estructura
      </v-card-title>
      <v-card-text>
        Por favor, señale el número de instancias académicas y
        administrativas reconocidas en el marco normativo y/u
        organigrama oficial de su institución.
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="survey_data.academic_instances"
              label="Instancias académicas"
              type="number"
              variant="outlined"
              class="mt-3"
            ></v-text-field>
          </v-col>
            <v-col cols="12" md="6">
            <v-text-field
              v-model="survey_data.admin_instances"
              label="Instancias administrativas"
              type="number"
              variant="outlined"
              class="mt-3"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>

    </v-card>
    <v-card variant="outlined" class="mt-4">
      <v-card-title class="text-secondary">
        Poblaciones
      </v-card-title>
      <v-card-text>
        Por favor, señale las poblaciones que integran a la comunidad de su IES,
        así como todas aquellas que están presentes física o
        virtualmente y/o mantiene vínculos a través de sus actividades
        institucionales.
        <v-input
          :model-value="survey_data.sectors"
          class="pb-2"
          :rules="[rules.has_content]"
        >
          <v-row
            align="start"
            class="my-2"
            no-gutters
          >
            <v-col
              v-for="sector in main_sectors"
              :key="sector.id"
              cols="12"
              class="px-0"
            >
              <v-checkbox
                v-model="survey_data.sectors"
                hide-details
                :value="sector.id"
                color="accent"
                xdensity="compact"
              >
                <template #label>
                  <div>
                    <div
                      class="text-subtitle-1 font-weight-medium"
                    >{{ sector.name }}</div>
                    <div
                      v-if="sector.description"
                      class="text-body-2 text-grey-darken-2"
                    >{{ sector.description }}</div>
                  </div>
                </template>
              </v-checkbox>
            </v-col>
          </v-row>
        </v-input>
      </v-card-text>
    </v-card>
    <v-card
      variant="outlined"
      class="mt-4"
    >
      <v-card-title class="text-secondary">
        Planes de estudio
      </v-card-title>
      <v-card-text>
        Por favor, señale el número de planes de estudio vigentes en su
        institución, de acuerdo con el nivel de estudios
        <v-row class="mt-3">
          <v-col
            v-for="plan_type in plan_types"
            :key="plan_type.key"
            cols="12"
            md="4"
          >
            <v-text-field
              v-model="survey_data[plan_type.key]"
              :label="`Planes de estudio ${plan_type.name}`"
              type="number"
              variant="outlined"
              :hint="plan_type.description"
              persistent-hint
              style="max-width: 400px;"

            ></v-text-field>
          </v-col>

        </v-row>
      </v-card-text>

    </v-card>
    <v-card-actions class="mt-4">
      <v-spacer></v-spacer>
      <v-btn
        color="primary"
        variant="elevated"

      >
        Guardar datos iniciales
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<style scoped>

</style>