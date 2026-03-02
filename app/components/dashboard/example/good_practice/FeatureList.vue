<script setup>
import { ref, computed, onMounted } from 'vue'
import FeatureItem from "~/components/dashboard/example/good_practice/FeatureItem.vue";

import { useMainStore } from '~/store/index.js'
const mainStore = useMainStore()
const { cats, cats_ready, all_nodes } = mainStore

const props = defineProps({
  goodPracticeId: { type: Number, required: true },
  featureValues: { type: Array, default: () => [] },
  isStaff: { type: Boolean, default: false }
})

const localValues = ref([])

// console.log("all_nodes.feature", all_nodes)

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
    <div
      v-if="!isStaff"
      class="mb-4 mt-4 text-h6"
    >
      Marca las características que crees que cumple tu buena práctica.

    </div>

    <template
      v-for="feature in all_nodes.features.children"
      :key="feature.id"
    >
      <FeatureItem
        v-if="!isStaff || getFeatureValue(feature.data.id)?.has_attribute"
        :feature="feature"
        :value="getFeatureValue(feature.data.id)"
        :is-staff="isStaff"
        @update="(data) => handleUpdate(feature.data.id, data)"
      />
    </template>
  </div>
</template>