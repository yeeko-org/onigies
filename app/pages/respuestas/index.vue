<script setup>
// import {nextTick, onBeforeMount, onMounted, ref, watch} from 'vue'
import { storeToRefs } from 'pinia';
import {useAuthStore} from "~/stores/auth.js";
import {useMainStore} from "~/stores/index.js";

const mainStore = useMainStore()
const authStore = useAuthStore()
const { ies_data } = storeToRefs(authStore);

definePageMeta({
  middleware: 'dashboard',
  layout: 'ies',
})

// rewrite the last line in typescript
// const current_filters = ref<Array<{name: string, order: number, init_visible?: boolean, collection?: string, is_collection?: boolean, disabled?: boolean}>>([])


</script>

<template>
  <v-card class="px-3 mt-3" >
    <v-card-title>
      Interactúa mediante el menú.


    </v-card-title>
    {{ies_data}}
  </v-card>
</template>