<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth.js'
import { useMainStore } from '~/stores/index.js'
import { useGoodPractice } from '~/composables/useGoodPractice.js'
import GoodPracticeCard from "~/components/dashboard/example/goodpractice/GoodPracticeCard.vue";
import GoodPracticeForm from "~/components/dashboard/example/goodpractice/GoodPracticeForm.vue";

const props = defineProps({
  goodPracticePackage: { type: Object, required: true }
})

const authStore = useAuthStore()
const { loading } = useGoodPractice()
const { fetchElements, getSimple } = useMainStore()

const isStaff = computed(() => authStore.is_staff)
const goodPractices = ref([])
const showForm = ref(false)
const selectedPractice = ref(null)

const canAddMore = computed(() => {
  return !isStaff.value && goodPractices.value.length < 5
})

const loadPractices = async () => {
  const result = await fetchElements(
    ['good_practice_package', props.goodPracticePackage.id]
  )
  goodPractices.value = result.good_practices
}

const openForm = (practice = null) => {
  selectedPractice.value = practice
  showForm.value = true
}

const closeForm = () => {
  showForm.value = false
  selectedPractice.value = null
}

const onSaved = () => {
  closeForm()
  loadPractices()
}

const onDeleted = () => {
  closeForm()
  loadPractices()
}

onMounted(loadPractices)
</script>

<template>
  <v-container fluid>
    <v-card>
      <v-card-title class="d-flex align-center flex-wrap ga-2">
        <v-icon start>mdi-lightbulb-on</v-icon>
        <span>Buenas Prácticas</span>
        <v-spacer />
        <v-chip
          :color="goodPractices.length >= 5 ? 'warning' : 'primary'"
          variant="flat"
        >
          {{ goodPractices.length }} / 5
        </v-chip>
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
          v-if="loading"
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
            md="6"
            lg="4"
          >
            <GoodPracticeCard
              :practice="practice"
              :is-staff="isStaff"
              @edit="openForm(practice)"
            />
          </v-col>
        </v-row>

        <v-btn
          v-if="canAddMore"
          color="primary"
          variant="tonal"
          block
          class="mt-4"
          @click="openForm()"
        >
          <v-icon start>mdi-plus</v-icon>
          Agregar Buena Práctica
        </v-btn>
      </v-card-text>
    </v-card>

    <v-dialog
      v-model="showForm"
      max-width="950"
      persistent
      scrollable
    >
      <GoodPracticeForm
        :practice="selectedPractice"
        :package-id="goodPracticePackage.id"
        :is-staff="isStaff"
        @close="closeForm"
        @saved="onSaved"
        @deleted="onDeleted"
      />
    </v-dialog>
  </v-container>
</template>