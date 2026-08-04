<script setup>
import {storeToRefs} from 'pinia';
import {useIesStore} from "~/store/ies.js";
import {useMainStore} from '~/store/index.js'
import FlowStatusChip from "~/components/dashboard/flow/FlowStatusChip.vue";
import GenericDisplay from "~/components/dashboard/common/select/GenericDisplay.vue";
import InstitutionCard from "~/components/dashboard/ies/institution/InstitutionCard.vue";
import {
  SECTION_BASE, SECTION_CP, SECTION_BP, isSectionVisible,
} from "~/utils/sections.js";

const iesStore = useIesStore()
const mainStore = useMainStore()
const { cats, cats_ready } = storeToRefs(mainStore)

definePageMeta({
  middleware: 'dashboard',
  layout: 'ies',
})

const showBase = computed(
  () => isSectionVisible(SECTION_BASE, iesStore.is_test))
const showCp = computed(
  () => isSectionVisible(SECTION_CP, iesStore.is_test))
const showBp = computed(
  () => isSectionVisible(SECTION_BP, iesStore.is_test))

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
                <NuxtLink
                  v-if="showBase"
                  class="chip-link mr-6"
                  :to="{
                    path: `/respuestas/${year.year}`,
                    query: { tab: 'base' },
                  }"
                >
                  <v-badge
                    color="transparent"
                    location="bottom right"
                    offset-x="74"
                    offset-y="-6"
                  >
                    <v-chip
                      color="blue-grey"
                      size="large"
                      class="px-6"
                      prepend-icon="assignment"
                    >
                      Datos base
                    </v-chip>
                    <template #badge>
                      <FlowStatusChip
                        :status="year.survey?.general_package?.status"
                        x-small
                      />
                    </template>
                  </v-badge>
                </NuxtLink>
                <NuxtLink
                  v-for="axis_value in (showCp && year.survey?.axis_values)
                    || []"
                  :key="axis_value.id"
                  class="chip-link mr-6"
                  :to="{
                    path: `/respuestas/${year.year}`,
                    query: { tab: `axis-${axis_value.axis}` },
                  }"
                >
                  <v-badge
                    color="transparent"
                    location="bottom right"
                    offset-x="74"
                    offset-y="-6"
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
                      <FlowStatusChip
                        :status="axis_value.status"
                        x-small
                      />
                    </template>
                  </v-badge>
                </NuxtLink>
                <NuxtLink
                  v-if="showBp && year.survey?.packages.length > 0"
                  class="chip-link"
                  :to="{
                    path: `/respuestas/${year.year}`,
                    query: { tab: 'bp' },
                  }"
                >
                  <v-badge
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
                      <FlowStatusChip
                        :status="year.survey.packages[0].status"
                        x-small
                      />
                    </template>
                  </v-badge>
                </NuxtLink>
              </div>
            </v-card-text>
          </v-card>
        </template>
      </v-card-text>
    </v-card>
  </v-row>
</template>

<style scoped>
.chip-link {
  text-decoration: none;
  cursor: pointer;
}
</style>