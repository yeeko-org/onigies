<script setup>

import {useMainStore} from "~/store/index.js";
import {useIesStore} from "~/store/ies.js";
import GoodPracticeList from
    "~/components/dashboard/example/good_practice/GoodPracticeList.vue";
import SurveyInitData from "~/components/dashboard/survey/SurveyInitData.vue";
const mainStore = useMainStore()
const iesStore = useIesStore()
const route = useRoute()

const tab = ref(null)
const period = computed(() => parseInt(route.params.period))

const all_axis = computed(() => mainStore.cats?.axis || [])

const current_survey = computed(() => {
  if (!iesStore.surveys)
    return null
  return iesStore.surveys.find(survey => survey.period === period.value)
})

</script>

<template>
  <v-card style="width: 100%">
    <v-card-title>
      Registro del año {{ iesStore.current_period }}
    </v-card-title>

    <v-tabs
      v-model="tab"
      align-tabs="center"
      color="deep-purple-accent-4"
    >
      <v-tab :value="0">Datos base</v-tab>
      <v-tab
        :value="8"
        color="pink"
        base-color="pink"
      >
        <v-icon left color="pink">
          lightbulb
        </v-icon>
        Buenas prácticas
      </v-tab>
<!--      <v-tab :value="1">City</v-tab>-->
      <v-tab
        v-for="axis in all_axis"
        :key="axis.id"
        :value="axis.id"
        :color="axis.color"
        :base-color="axis.color"
        disabled
      >
        <v-icon left :color="axis.color">
          {{ axis.icon }}
        </v-icon>
        {{ axis.short_name }}
      </v-tab>
    </v-tabs>
<!--    <v-progress-linear-->
<!--      v-if="iesStore.loading_ies_data"-->
<!--      indeterminate-->
<!--      height="20"-->
<!--      color="primary"-->
<!--    ></v-progress-linear>-->

    <v-tabs-window v-if="iesStore.ies_data" v-model="tab">
      <v-tabs-window-item
        :value="0"
      >
        <v-container fluid>
          <SurveyInitData
            :period="period"
            :survey_id="current_survey?.id"
          />
        </v-container>

      </v-tabs-window-item>

      <v-tabs-window-item
        v-for="axis in all_axis"
        :key="axis.id"
        :value="axis.id"
      >
        <v-container fluid>
          <v-row>
            <v-col
              v-for="i in 6"
              :key="i"
              cols="12"
              md="4"
            >
              <v-img
                :lazy-src="`https://picsum.photos/10/6?image=${i * n * 5 + 10}`"
                :src="`https://picsum.photos/500/300?image=${i * n * 5 + 10}`"
                height="205"
                cover
              ></v-img>
            </v-col>
          </v-row>
        </v-container>
      </v-tabs-window-item>
      <v-tabs-window-item
        :value="8"
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