<script setup>
import { computed } from 'vue'
import StatusChip from "~/components/dashboard/status/StatusChip.vue";
import {useMainStore} from "~/stores/index.js";
import TitleCommon from "~/components/dashboard/generic/TitleCommon.vue";
import GoodPracticeForm from "~/components/dashboard/example/goodpractice/GoodPracticeForm.vue";
import SelectGroup from "~/components/dashboard/common/select/SelectGroup.vue";
const mainStore = useMainStore()

const props = defineProps({
  practice: { type: Object, required: true },
  isStaff: { type: Boolean, default: false }
})

const emit = defineEmits(['edit'])

const active_features = computed(() => {
  return (props.practice.feature_values || []).filter(f => f.has_attribute)
})

const evaluatedCount = computed(() => {
  const features = props.practice.feature_values || []
  return features.filter(
    f => f.has_attribute && f.final_option
  ).length
})

const features_dict = computed(() => {
  return mainStore.cats.feature.reduce((acc, feature) => {
    acc[feature.id] = feature
    return acc
  }, {})
})

</script>

<template>
  <v-sheet
    elevation="4"
    :class="{'pa-3': practice.in_edition}"
    rounded="lg"
  >
    <v-card
      :hover="!practice.in_edition"
      :class="{'cursor-pointer': !practice.in_edition}"
      variant="tonal"
      color="blue"
    >
      <v-card-title
        class="text-subtitle-1 font-weight-bold d-flex align-center ga-2"
      >
        <v-icon start size="small" color="primary">
          lightbulb
        </v-icon>
        <TitleCommon
          :title_text="practice.name || 'Sin nombre'"
          color="indigo"
          variant="text"
          tile
        />
  <!--      <StatusDetail-->
  <!--        collection="register"-->
  <!--        :final_filters="practice"-->
  <!--        hide_details-->
  <!--      />-->
          <v-chip variant="tonal" color="success" class="ml-3">
            <v-icon start size="small">check_circle</v-icon>
            {{ active_features.length }} características
            <v-tooltip
              activator="parent"
              location="top"
            >
              <div>
                Características activas:
                <div v-for="feature in active_features" :key="feature.id">
                  - {{ features_dict[feature.feature].name }}
                </div>
              </div>
            </v-tooltip>
          </v-chip>
          <v-chip
            v-if="isStaff"
            size="small"
            variant="tonal"
            :color="evaluatedCount === active_features.length
              ? 'success' : 'warning'"
          >
            <v-icon start size="x-small">assignment_turned_in</v-icon>
            {{ evaluatedCount }}/{{ active_features.length }} evaluados
          </v-chip>
        <v-spacer></v-spacer>
        <StatusChip
          collection="register"
          :main="practice"
          class="ml-4"
        />


      </v-card-title>

      <v-card-text>
        <div class="d-flex flex-wrap ga-2 align-center mb-3">
          <SelectGroup
            filter_group_name="axes"
            :main_object="practice"
            forced_level="subtype"
            is_display
          />
        </div>

        <template v-if="!practice.in_edition">
          <p
            v-if="practice.description"
            class="text-body-2 text-medium-emphasis mb-3 text-truncate-2"
          >
            <b class="mr-1">Descripción:</b>
            <span v-html="practice.description"></span>
          </p>
          <p
            v-if="practice.results"
            class="text-body-2 text-medium-emphasis mb-3 text-truncate-2"
          >
            <b class="mr-1">Resultados:</b>
            <span v-html="practice.results"></span>
          </p>
        </template>


      </v-card-text>

      <v-card-actions v-if="!practice.in_edition">
        <v-spacer/>
        <v-btn
          color="primary"
          variant="text"
          @click="practice.in_edition = true;"
        >
          {{ isStaff ? 'Evaluar' : 'Editar' }}
        </v-btn>
        <v-spacer/>
      </v-card-actions>
    </v-card>
    <GoodPracticeForm
      v-if="practice.in_edition"
      :practice="practice"
      :package-id="practice.package"
      class="mt-3"
      @saved="emit('edit', $event)"
    />

  </v-sheet>
</template>

<style scoped>
.text-truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>