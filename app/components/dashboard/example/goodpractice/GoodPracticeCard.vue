<script setup>
import { computed } from 'vue'

const props = defineProps({
  practice: { type: Object, required: true },
  isStaff: { type: Boolean, default: false }
})

const emit = defineEmits(['edit'])

const featuresCount = computed(() => {
  const features = props.practice.feature_values || []
  const active = features.filter(f => f.has_attribute).length
  return { active, total: features.length }
})

const evaluatedCount = computed(() => {
  const features = props.practice.feature_values || []
  return features.filter(
    f => f.has_attribute && f.final_option
  ).length
})
</script>

<template>
  <v-card
    class="h-100 cursor-pointer"
    hover
    @click="emit('edit')"
  >
    <v-card-title class="text-subtitle-1 font-weight-bold">
      <v-icon start size="small" color="primary">
        mdi-star-circle
      </v-icon>
      {{ practice.name || 'Sin nombre' }}
    </v-card-title>

    <v-card-text>
      <p
        v-if="practice.description"
        class="text-body-2 text-medium-emphasis mb-3 text-truncate-2"
      >
        {{ practice.description }}
      </p>

      <div class="d-flex flex-wrap ga-2">
        <v-chip size="small" variant="tonal">
          <v-icon start size="x-small">mdi-axis-arrow</v-icon>
          {{ practice.axis?.short_name || 'Sin eje' }}
        </v-chip>
        <v-chip size="small" variant="tonal" color="secondary">
          <v-icon start size="x-small">mdi-check-circle</v-icon>
          {{ featuresCount.active }}/{{ featuresCount.total }}
        </v-chip>
        <v-chip
          v-if="isStaff"
          size="small"
          variant="tonal"
          :color="evaluatedCount === featuresCount.active
            ? 'success' : 'warning'"
        >
          <v-icon start size="x-small">mdi-clipboard-check</v-icon>
          {{ evaluatedCount }}/{{ featuresCount.active }} evaluados
        </v-chip>
      </div>
    </v-card-text>

    <v-card-actions>
      <v-spacer />
      <v-btn
        size="small"
        color="primary"
        variant="text"
        @click.stop="emit('edit')"
      >
        {{ isStaff ? 'Evaluar' : 'Editar' }}
        <v-icon end>mdi-chevron-right</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<style scoped>
.text-truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>