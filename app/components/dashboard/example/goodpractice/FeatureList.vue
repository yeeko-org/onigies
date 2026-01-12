<script setup>
import { ref, computed, onMounted } from 'vue'
import { useGoodPractice } from '~/composables/useGoodPractice.js'

const props = defineProps({
  goodPracticeId: { type: Number, required: true },
  features: { type: Array, default: () => [] },
  featureValues: { type: Array, default: () => [] },
  isStaff: { type: Boolean, default: false }
})

const { saveFeatureGoodPractice } = useGoodPractice()
const localValues = ref([])

const getFeatureValue = (featureId) => {
  return localValues.value.find(fv => {
    const fvFeatureId = fv.feature?.id || fv.feature
    return fvFeatureId === featureId
  }) || null
}

const initializeValues = () => {
  localValues.value = props.features.map(feature => {
    const existing = props.featureValues.find(fv => {
      const fvFeatureId = fv.feature?.id || fv.feature
      return fvFeatureId === feature.id
    })
    return existing || {
      good_practice: props.goodPracticeId,
      feature: feature.id,
      has_attribute: false,
      justification: '',
      final_option: null
    }
  })
}

const activeFeatures = computed(() => {
  return props.features.filter(f => {
    const value = getFeatureValue(f.id)
    return value?.has_attribute
  })
})

const handleUpdate = async (featureId, data) => {
  const idx = localValues.value.findIndex(v => {
    const vFeatureId = v.feature?.id || v.feature
    return vFeatureId === featureId
  })
  if (idx !== -1) {
    const updated = { ...localValues.value[idx], ...data }
    try {
      const result = await saveFeatureGoodPractice(updated)
      localValues.value[idx] = result
    } catch (e) {
      console.error('Error al guardar característica:', e)
    }
  }
}

onMounted(initializeValues)
</script>

<template>
  <div>
    <v-alert
      v-if="isStaff && !activeFeatures.length"
      type="info"
      variant="tonal"
      class="mb-4"
    >
      La IES no ha marcado ninguna característica como cumplida.
    </v-alert>

    <v-expansion-panels variant="accordion">
      <template v-for="feature in features" :key="feature.id">
        <FeatureItem
          v-if="!isStaff || getFeatureValue(feature.id)?.has_attribute"
          :feature="feature"
          :value="getFeatureValue(feature.id)"
          :is-staff="isStaff"
          @update="(data) => handleUpdate(feature.id, data)"
        />
      </template>
    </v-expansion-panels>

    <v-alert
      v-if="!features.length"
      type="warning"
      variant="tonal"
      class="mt-4"
    >
      No hay características configuradas.
    </v-alert>
  </div>
</template>