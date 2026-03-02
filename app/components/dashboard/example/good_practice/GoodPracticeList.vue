<script setup>
import {ref, computed, onMounted, watch} from 'vue'
import { useAuthStore } from '~/store/auth.js'
import { useIesStore } from "~/store/ies.js";
import { useMainStore } from '~/store/index.js'
import GoodPracticeCard from "~/components/dashboard/example/good_practice/GoodPracticeCard.vue";
import NewGoodPractice from "~/components/dashboard/example/good_practice/NewGoodPractice.vue";

const props = defineProps({
  packageId: { type: Number, required: false },
  period: { type: Number, required: false }
})

const authStore = useAuthStore()
const { getSimple, saveSimple, saveAction, status_dict } = useMainStore()
const mainStore = useMainStore()
const iesStore = useIesStore()

const isStaff = computed(() => authStore.is_staff)
const goodPracticePackage = ref({
  has_good_practices: null,
})
const goodPractices = ref([])
const create_dialog = ref(false)
const current_loading = ref(false)

const limit_reached = computed(() => {
  return goodPractices.value.length >= 5
})

const edition_available = computed(()=> {
  if (isStaff.value)
    return false
  else {
    return status_sending.value.role === 'ies'
  }
})

const canAddMore = computed(() => {
  if (isStaff.value)
    return false
  if (!edition_available.value)
    return false
  return goodPracticePackage.value.has_good_practices && !limit_reached.value
})

const package_id = computed(() => {
  if (props.packageId)
    return props.packageId
  // if (!iesStore.ies_data)
  //   return null
  return iesStore.all_packages.find(p=>p.period === props.period)?.id

})

const loadPractices = async () => {
  current_loading.value = true
  const result = await getSimple(
    ['good_practice_package', package_id.value]
  )
  // console.log("Result good practices:", result)
  if (result && result.good_practices){
    goodPracticePackage.value = result
    setPractices(result.good_practices)
  }
  current_loading.value = false
}

function setPractices(newPractices) {
  goodPractices.value = newPractices.map(gp => ({
    ...gp,
    in_edition: false
  }))
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

function deletePractice(practice) {
  const idx = goodPractices.value.findIndex(p => p.id === practice.id)
  if (idx !== -1) {
    goodPractices.value.splice(idx, 1)
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

function editPackage() {
  current_loading.value = true
  saveSimple(['good_practice_package', goodPracticePackage.value]).then(res=>{
    goodPracticePackage.value = res
    current_loading.value = false
  }).catch(e=>{
    console.error("Error updating package:", e)
    current_loading.value = false
  })
}

const send_dialog = ref(false)
function wantSend() {
  send_dialog.value = true
}

function sendPackage(){
  saveAction(['good_practice_package', package_id.value, 'send']).then(res=>{
    goodPracticePackage.value = res
    setPractices(res.good_practices)
    send_dialog.value = false
  }).catch(e=>{
    console.error("Error sending package:", e)
  })
}

const status_sending = computed(()=> {
  if (!mainStore.status_dict.sending)
    return {}
  return mainStore.status_dict.sending[goodPracticePackage.value.status_sending] || {}
})

</script>

<template>
  <v-card elevation="6" class="pa-3">
    <v-card-title class="d-flex align-center flex-wrap ga-2">
      <v-icon start>lightbulb</v-icon>
      <span>
        Buenas prácticas
        <template v-if="goodPractices.length && false">
          ({{ goodPractices.length }})
        </template>
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
        <span v-else-if="edition_available">
          (Puedes agregar hasta 5 buenas prácticas)
        </span>
      </v-chip>
      <v-btn
        v-if="canAddMore"
        color="accent"
        variant="elevated"
        @click="openNewForm()"
        prepend-icon="add"
      >
        Agregar
      </v-btn>
<!--        <StatusDetail-->
<!--          v-if="!isStaff"-->
<!--          model="goodpracticepackage"-->
<!--          field="status_sending"-->
<!--          :item-id="goodPracticePackage.id"-->
<!--        />-->
    </v-card-title>
    <v-alert
      v-if="!isStaff && status_sending.role !== 'ies'"
      type="success"
    >
      Las buenas prácticas han sido enviadas y están en revisión.
      Espera los resultados.
    </v-alert>

    <v-card-text class="text-subtitle-1 mt-3 mb-1 d-flex">
      <div class="text-indigo">
        ¿Durante los últimos tres años, su institución ha implementado
        alguna política, programa o acción en materia de igualdad de género,
        no discriminación, cuidados corresponsables y/o
        una vida libre de violencias que, por su trascendencia o innovación,
        considere que constituya una práctica exitosa
        que pudiera ser compartida a nivel nacional?
      </div>
      <v-spacer></v-spacer>
      <v-radio-group
        v-model="goodPracticePackage.has_good_practices"
        style="width: 680px;"
        class="ml-3"
        @update:modelValue="editPackage"
        :readonly="!edition_available"
      >
        <v-radio
          class="mr-3"
          :label="`Sí tengo buenas prácticas`"
          :value="true"
        />
        <v-radio
          :label="`No / No deseo responder`"
          :value="false"
        />
      </v-radio-group>
    </v-card-text>

    <v-divider />
    <v-card-text v-if="goodPracticePackage.has_good_practices">
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
          v-for="(practice, index) in goodPractices"
          :key="practice.id"
          cols="12"
        >

          <GoodPracticeCard
            v-model="goodPractices[index]"
            :is-staff="isStaff"
            :sent-at="goodPracticePackage.sent_at"
            :edition-available="edition_available"
            @edit="editPractice($event, practice)"
            @deleted="deletePractice(practice)"
          />

        </v-col>
      </v-row>

    </v-card-text>
    <v-card-actions
      v-if="goodPracticePackage.has_good_practices && edition_available"
      class="mb-3 mx-3"
    >
      <v-btn
        v-if="canAddMore"
        color="accent"
        variant="outlined"
        @click="openNewForm()"
        prepend-icon="add"
      >
        Agregar
      </v-btn>

      <v-spacer></v-spacer>
      <v-btn
        color="accent"
        variant="elevated"
        append-icon="send"
        @click="wantSend"
        size="large"
        class="px-6"
      >
        Enviar buenas prácticas
      </v-btn>
    </v-card-actions>
    <v-dialog
      v-model="create_dialog"
      max-width="600"
      persistent
      scrollable
    >
      <NewGoodPractice
        :package-id="package_id"
        :is-staff="true"
        @close="create_dialog = false"
        @created="onCreated"
      />
    </v-dialog>
    <v-dialog
      v-model="send_dialog"
      max-width="500"
    >
      <v-card>
        <v-card-title class="headline text-no-wrap no-wrap">
          ¿Desea enviar a revisión las buenas prácticas?
        </v-card-title>
        <v-card-text cxlass="text-grey-darken-2">
          <v-alert
            color="info"
            border="start"
            variant="outlined"
          >

            Una vez enviadas, no podrás realizar modificaciones o agregar nuevas.
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-btn
            color="error"
            variant="outlined"
            @click="send_dialog = false"
          >
            Cancelar envio
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            color="accent"
            variant="elevated"
            @click="sendPackage"
            append-icon="send"
            class="px-6"
          >
            Sí enviar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>

</template>

<style scoped>
.no-wrap{
  word-break: normal !important;
}
</style>