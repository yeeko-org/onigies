<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth.js'
import { useMainStore } from '~/stores/index.js'
import GoodPracticeCard from "~/components/dashboard/example/goodpractice/GoodPracticeCard.vue";
import NewGoodPractice from "~/components/dashboard/example/goodpractice/NewGoodPractice.vue";

const props = defineProps({
  goodPracticePackage: { type: Object, required: true }
})

const authStore = useAuthStore()
const { getSimple } = useMainStore()

const isStaff = computed(() => authStore.is_staff)
const goodPractices = ref([])
const create_dialog = ref(false)
const current_loading = ref(false)

const limit_reached = computed(() => {
  return goodPractices.value.length >= 5
})

const canAddMore = computed(() => {
  return !isStaff.value && !limit_reached.value
})

const loadPractices = async () => {
  current_loading.value = true
  const result = await getSimple(
    ['good_practice_package', props.goodPracticePackage.id]
  )
  // console.log("Result good practices:", result)
  if (result && result.good_practices){
    goodPractices.value = result.good_practices.map(gp => ({
      ...gp,
      in_edition: false
    }))
  }
  current_loading.value = false
}

onMounted(loadPractices)

function editPractice(new_value, practice) {
  const idx = goodPractices.value.findIndex(p => p.id === practice.id)
  if (idx !== -1) {
    goodPractices.value[idx] = {
      ...new_value,
      in_edition: false
    }
  }
}

const openNewForm = () => {
  create_dialog.value = true
}

const onCreated = (new_practice) => {
  new_practice.in_edition = true
  goodPractices.value.push(new_practice)
  create_dialog.value = false
}


</script>

<template>
  <v-card>
    <v-card-title class="d-flex align-center flex-wrap ga-2">
      <v-icon start>lightbulb</v-icon>
      <span>
        Buenas Prácticas
        ({{ goodPractices.length }})
      </span>
      <v-spacer />
      <v-chip
        variant="text"
        color="grey-darken-1"
      >
        <span
          v-if="limit_reached"
        >
          Has alcanzado el límite de buenas prácticas.
        </span>
        <span v-else>
          (Puedes agregar hasta 5 buenas prácticas)
        </span>
      </v-chip>
      <v-btn
        v-if="canAddMore"
        color="accent"
        variant="elevated"
        @click="openNewForm()"
      >
        <v-icon start>add</v-icon>
        Agregar
      </v-btn>
<!--        <StatusDetail-->
<!--          v-if="!isStaff"-->
<!--          model="goodpracticepackage"-->
<!--          field="status_sending"-->
<!--          :item-id="goodPracticePackage.id"-->
<!--        />-->
    </v-card-title>

    <v-divider />

    <v-card-text>
      <v-progress-linear
        v-if="current_loading"
        indeterminate
        color="primary"
      />
      <v-alert
        v-else-if="!goodPractices.length"
        type="info"
        variant="tonal"
      >
        No hay buenas prácticas registradas.
      </v-alert>

      <v-row v-else>
        <v-col
          v-for="practice in goodPractices"
          :key="practice.id"
          cols="12"
        >
          <GoodPracticeCard
            :practice="practice"
            :is-staff="isStaff"
            @edit="editPractice($event, practice)"
          />

        </v-col>
      </v-row>


    </v-card-text>
    <v-dialog
      v-model="create_dialog"
      max-width="950"
      persistent
      scrollable
    >
      <NewGoodPractice
        :package-id="goodPracticePackage.id"
        :is-staff="isStaff"
        @close="create_dialog = false"
        @created="onCreated"
      />
    </v-dialog>
  </v-card>

</template>