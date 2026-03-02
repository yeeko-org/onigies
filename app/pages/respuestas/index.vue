<script setup>
import {storeToRefs} from 'pinia';
import {useIesStore} from "~/store/ies.js";
import {useMainStore} from '~/store/index.js'
import StatusChip from "~/components/dashboard/status/StatusChip.vue";
import GenericDisplay from "~/components/dashboard/common/select/GenericDisplay.vue";
import InstitutionCard from "~/components/dashboard/ies/institution/InstitutionCard.vue";

const iesStore = useIesStore()
const mainStore = useMainStore()
const { cats, cats_ready } = storeToRefs(mainStore)

definePageMeta({
  middleware: 'dashboard',
  layout: 'ies',
})



</script>

<template>
  <v-row no-gutters>
    <InstitutionCard/>
    <v-divider></v-divider>
    <v-card class="w-100 mb-4" variant="text">
      <v-card-title class="text-h5 font-weight-bold">
        Respuestas por año
      </v-card-title>
      <v-card-text v-if="cats_ready">
        <template
          v-for="year in iesStore.available_years"
          :key="year"
        >
<!--          <v-list-item-->
<!--            base-color="primary"-->
<!--            :title="`Respuestas ${year}`"-->
<!--            :to="`/respuestas/${year}`"-->
<!--          ></v-list-item>-->
<!--          <v-divider></v-divider>-->
          <v-card

            variant="tonal"
            color="primary"
            class="mb-3"
          >
            <v-card-title class="d-flex align-center">
              Año {{ year.year }}
              <br>
              <v-spacer />
              <NuxtLink
                :to="`/respuestas/${year.year}`"
              >
                <v-btn
                  color="accent"
                  variant="outlined"
                >
                  Ver respuestas
                </v-btn>
              </NuxtLink>
            </v-card-title>
            <v-card-text class="pb-10">
              <div
                class="d-flex align-center flex-wrap"
              >
                <v-badge
                  v-for="axis_value in year.survey?.axis_values || []"
                  :key="axis_value.id"
                  color="transparent"
                  location="bottom right"
                  offset-x="74"
                  offset-y="-6"
                  class="mr-6"
                >
                  <GenericDisplay
                    :element_value="axis_value.axis"
                    level="group"
                    :items="cats.axis"
                    show_name
                    hide_border
                    item_title="short_name"
                    size="large"
                    class="px-6"
                  />
                  <template #badge>
                    <StatusChip
                      collection="register"
                      :main="axis_value"
                      hide_details
                    />

                  </template>
                </v-badge>
                <v-badge
                  v-if="year.package"
                  color="transparent"
                  location="bottom right"
                  offset-x="74"
                  offset-y="-6"
                >
                  <v-chip
                    color="pink"
                    size="large"
                    class="px-6"
                    prepend-icon="lightbulb"
                  >
                    Buenas prácticas
                  </v-chip>

                  <template #badge>
                    <StatusChip
                      collection="sending"
                      :main="year.package"
                      hide_details
                    />
                  </template>
                </v-badge>
              </div>
            </v-card-text>
          </v-card>
        </template>
      </v-card-text>
    </v-card>
  </v-row>
</template>