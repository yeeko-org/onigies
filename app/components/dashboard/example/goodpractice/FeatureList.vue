<script setup>
import { ref, computed, onMounted } from 'vue'
import FeatureItem from "~/components/dashboard/example/goodpractice/FeatureItem.vue";

import { useMainStore } from '~/stores/index.js'
const mainStore = useMainStore()
const { cats, cats_ready } = mainStore

const props = defineProps({
  goodPracticeId: { type: Number, required: true },
  featureValues: { type: Array, default: () => [] },
  isStaff: { type: Boolean, default: false }
})

// const { saveFeatureGoodPractice } = useGoodPractice()
const localValues = ref([])

const getFeatureValue = (featureId) => {
  return localValues.value.find(fv => {
    const fvFeatureId = fv.feature?.id || fv.feature
    return fvFeatureId === featureId
  }) || null
}

const initializeValues = () => {
  localValues.value = cats.feature.map(feature => {
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
  return cats.feature.filter(f => {
    const value = getFeatureValue(f.id)
    return value?.has_attribute
  })
})

const handleUpdate = async (featureId, data) => {
  // console.log("Updating feature:", featureId, data)
  const idx = localValues.value.findIndex(v => {
    const vFeatureId = v.feature?.id || v.feature
    return vFeatureId === featureId
  })
  if (idx !== -1) {
    const updated = { ...localValues.value[idx], ...data }
    try {
      localValues.value[idx] = await mainStore.saveSimple(
        ['feature_good_practice', updated])
    } catch (e) {
      console.error('Error al guardar característica:', e)
    }
  }
}

onMounted(initializeValues)

</script>

<template>
  <div v-if="cats_ready">
    <v-alert
      v-if="isStaff && !activeFeatures.length"
      type="info"
      variant="tonal"
      class="mb-4"
    >
      La IES no ha marcado ninguna característica como cumplida.
    </v-alert>
    <v-alert
      v-if="!isStaff"
      type="info"
      variant="tonal"
      class="mb-4"
    >
      Marca las características que crees que cumple tu buena práctica.
    </v-alert>

    <template v-for="feature in cats.feature" :key="feature.id">
      <FeatureItem
        v-if="!isStaff || getFeatureValue(feature.id)?.has_attribute"
        :feature="feature"
        :value="getFeatureValue(feature.id)"
        :is-staff="isStaff"
        @update="(data) => handleUpdate(feature.id, data)"
      />
    </template>
  </div>
</template>