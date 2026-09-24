<script setup>

import {useMainStore} from "~/store/index.js";
import {useIesStore} from "~/store/ies.js";
import GoodPracticeList from
    "~/components/dashboard/example/good_practice/GoodPracticeList.vue";
import GeneralGroupList from
    "~/components/dashboard/survey/GeneralGroupList.vue";
import CpAxisCapture from
    "~/components/dashboard/answer/capture/CpAxisCapture.vue";
import {
  SECTION_BASE, SECTION_CP, SECTION_BP, isSectionVisible, sectionOfTab,
} from "~/utils/sections.js";
const mainStore = useMainStore()
const iesStore = useIesStore()
const route = useRoute()
const router = useRouter()

const period = computed(() => parseInt(route.params.period))

const all_axis = computed(() => mainStore.cats?.axis || [])

const showBase = computed(
  () => isSectionVisible(SECTION_BASE, iesStore.is_test))
const showCp = computed(
  () => isSectionVisible(SECTION_CP, iesStore.is_test))
const showBp = computed(
  () => isSectionVisible(SECTION_BP, iesStore.is_test))

// Primera sección visible en el orden en que se presentan; es a donde cae
// la IES real cuando su `?tab=` apunta a una sección que aún no se abre.
const default_tab = computed(() => {
  if (showBase.value) return SECTION_BASE
  if (showCp.value && all_axis.value.length)
    return `axis-${all_axis.value[0].id}`
  return SECTION_BP
})

// Las pestañas dependen de dos cargas que el middleware no espera: el perfil
// (`is_test` decide si se ve cp) y los catálogos (los ejes). Antes de
// tenerlas, v-tabs y v-tabs-window, que siempre fuerzan un valor elegido,
// caían en la primera pestaña y la escribían en la URL, pisando el `?tab=`
// de un deep-link recargado.
const ready = computed(() => !!iesStore.ies_data && mainStore.cats_ready)

const tabExists = (value) => !String(value).startsWith('axis-')
  || all_axis.value.some((axis) => `axis-${axis.id}` === value)

const tab = computed({
  get: () => {
    const current = route.query.tab
    const section = sectionOfTab(current)
    if (section && isSectionVisible(section, iesStore.is_test)
      && tabExists(current))
      return current
    return default_tab.value
  },
  set: (val) => {
    if (!ready.value || val === route.query.tab) return
    router.replace({ query: { ...route.query, tab: val } })
  },
})

const current_survey = computed(() => {
  if (!iesStore.surveys)
    return null
  return iesStore.surveys.find(survey => survey.period === period.value)
})

// El AxisValue del eje en el survey del periodo (llega en el perfil).
function axisValueOf(axisId) {
  return (current_survey.value?.axis_values || [])
    .find((av) => av.axis === axisId) || null
}

</script>

<template>
  <v-card style="width: 100%">
    <v-card-title>
      Registro del año {{ iesStore.current_period }}
    </v-card-title>

    <v-progress-linear v-if="!ready" indeterminate color="primary" />
    <v-tabs
      v-else
      v-model="tab"
      align-tabs="center"
      color="deep-purple-accent-4"
    >
      <v-tab v-if="showBase" value="base">
        Información base
      </v-tab>
      <template v-if="showCp">
        <v-tab
          v-for="axis in all_axis"
          :key="axis.id"
          :value="`axis-${axis.id}`"
          :color="axis.color"
          :base-color="axis.color"
        >
          <v-icon left :color="axis.color">
            {{ axis.icon }}
          </v-icon>
          {{ axis.short_name }}
        </v-tab>
      </template>
      <v-tab
        v-if="showBp"
        value="bp"
        color="pink"
        base-color="pink"
      >
        <v-icon left color="pink">
          lightbulb
        </v-icon>
        Buenas prácticas
      </v-tab>
    </v-tabs>
<!--    <v-progress-linear-->
<!--      v-if="iesStore.loading_ies_data"-->
<!--      indeterminate-->
<!--      height="20"-->
<!--      color="primary"-->
<!--    ></v-progress-linear>-->

    <v-tabs-window v-if="ready" v-model="tab">
      <v-tabs-window-item
        v-if="showBase"
        value="base"
      >
        <v-container fluid>
          <GeneralGroupList :survey="current_survey?.id" />
        </v-container>

      </v-tabs-window-item>

      <template v-if="showCp">
        <v-tabs-window-item
          v-for="axis in all_axis"
          :key="axis.id"
          :value="`axis-${axis.id}`"
        >
          <v-container fluid>
            <CpAxisCapture
              v-if="axisValueOf(axis.id)"
              :axis-value-id="axisValueOf(axis.id).id"
            />
            <v-alert v-else type="info" variant="tonal">
              Este eje aún no tiene cuestionario para este periodo.
            </v-alert>
          </v-container>
        </v-tabs-window-item>
      </template>
      <v-tabs-window-item
        v-if="showBp"
        value="bp"
      >
        <v-container fluid>
          <GoodPracticeList
            :period="period"
          />
        </v-container>

      </v-tabs-window-item>

    </v-tabs-window>
  </v-card>
</template>

<style scoped>

</style>