<script setup>
import { computed } from 'vue'
import FlowStatusChip from "~/components/dashboard/flow/FlowStatusChip.vue";
import FlowCommentIcon from "~/components/dashboard/flow/FlowCommentIcon.vue";
import {useMainStore} from "~/store/index.js";
import TitleCommon from "~/components/dashboard/common/utils/TitleCommon.vue";
import DisplayGroup from "~/components/dashboard/common/select/DisplayGroup.vue";
const mainStore = useMainStore()

const { practice, isStaff, editionAvailable, loading } = defineProps({
  practice: { type: Object, required: true },
  isStaff: { type: Boolean, default: false },
  sentAt: String,
  editionAvailable: Boolean,
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['open'])

const active_features = computed(() => {
  return (practice.feature_values || []).filter(f => f.has_attribute)
})

const evaluatedCount = computed(() => {
  const features = practice.feature_values || []
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

function openEdit(){
  if (!editionAvailable && !isStaff) return
  emit('open', practice.id)
}

</script>

<template>
  <v-sheet
    elevation="4"
    rounded="lg"
  >
    <v-card
      :hover="editionAvailable || isStaff"
      :class="{'cursor-pointer': editionAvailable || isStaff}"
      :loading="loading"
      variant="tonal"
      color="blue"
      @click="openEdit"
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
            {{ active_features.length }}
            característica{{active_features.length === 1 ? '' : 's'}}
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
            v-if="practice.evidences.length > 0"
            variant="tonal"
            color="blue-grey"
            class="ml-3"
            prepend-icon="attach_file"
          >
            {{practice.evidences.length}} archivos de evidencia
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
        <FlowCommentIcon :events="practice.flow_events" />
        <FlowStatusChip
          :status="practice.status"
          size="small"
          class="ml-4"
        />
      </v-card-title>

      <v-card-text>
        <div class="d-flex flex-wrap ga-2 align-center mb-3">
          <DisplayGroup
            :main_object="practice"
            filter_group_name="axes"
            forced_level="subtype"
          />
        </div>

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


      </v-card-text>
      <v-card-actions
        v-if="editionAvailable || isStaff"
      >
        <v-spacer/>
        <v-btn
          color="primary"
          variant="text"
          :loading="loading"
          @click.stop="openEdit"
        >
          {{ isStaff
            ? 'Evaluar'
            : (editionAvailable ? 'Editar' : 'Ver detalles') }}
        </v-btn>
        <v-spacer/>
      </v-card-actions>
    </v-card>

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