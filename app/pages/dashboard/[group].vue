<script setup>
import {useMainStore} from '~/stores/index'

import {storeToRefs} from "pinia";
import CollectionDisplay from "~/components/dashboard/CollectionDisplay.vue";

const mainStore = useMainStore()
const {
  cats_ready,
} = storeToRefs(mainStore)


// onMounted(() => {
//   console.log("onMounted", cats_ready.value)
// //   if (cats_ready.value) {
// //     changeFilters()
// //   }
// })
// watch(cats_ready, (newVal) => {
//   console.log("cats_ready", newVal)
//   if (newVal) {
//     changeFilters()
//   }
// })

</script>

<template>
  <CollectionDisplay
    v-if="cats_ready"
  />

</template>
