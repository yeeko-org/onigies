<script setup>
import { computed } from 'vue'
import FeatureItem from "~/components/dashboard/example/good_practice/FeatureItem.vue";

import { useMainStore } from '~/store/index.js'
const mainStore = useMainStore()
const { cats, cats_ready, all_nodes } = mainStore

const props = defineProps({
  goodPracticeId: { type: Number, required: true },
  isStaff: { type: Boolean, default: false },
  // Edición habilitada solo cuando es turno del usuario (IES o revisora). En
  // false, la calificación queda en solo lectura.
  editable: { type: Boolean, default: true }
})

const featureValues = defineModel('featureValues', {
  type: Array,
  default: () => []
})

const featureIdOf = fv => fv.feature?.id || fv.feature

const findIndex = featureId =>
  featureValues.value.findIndex(fv => featureIdOf(fv) === featureId)

const getFeatureValue = featureId => {
  const existing = featureValues.value.find(
    fv => featureIdOf(fv) === featureId)
  if (existing) return existing
  return {
    good_practice: props.goodPracticeId,
    feature: featureId,
    has_attribute: false,
    justification: '',
    final_option: null
  }
}

const activeFeatures = computed(() =>
  cats.feature.filter(f => getFeatureValue(f.id)?.has_attribute))

const handleUpdate = async (featureId, data) => {
  const current = getFeatureValue(featureId)
  const updated = { ...current, ...data }
  try {
    const saved = await mainStore.saveSimple(
      ['feature_good_practice', updated], 
        'No se pudo guardar la calificación de la característica.')
    if (saved.errors) return
    const idx = findIndex(featureId)
    if (idx !== -1)
      featureValues.value[idx] = saved.data
    else
      featureValues.value.push(saved.data)
  } catch (e) {
    devWarn('Error al guardar característica:', e)
  }
}

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
        :editable="editable"
        @update="(data) => handleUpdate(feature.data.id, data)"
      />
    </template>
  </div>
</template>