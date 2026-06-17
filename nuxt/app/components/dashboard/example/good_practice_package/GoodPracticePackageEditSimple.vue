<script setup>
/**
 * Vista de revisión de un GoodPracticePackage (dashboard / revisora).
 * El dashboard la auto-carga inline para la colección GoodPracticePackage
 * (convención {Model}EditSimple), pasándole solo v-model="full_main".
 *
 * Muestra: cabecera (institución / periodo / fecha de envío), status actual,
 * transiciones del motor para la revisora, comentarios del paquete y la lista
 * de prácticas en solo-lectura.
 *
 * NO incluye la pregunta has_good_practices ni el envío/descartar: eso es del
 * mundo de la IES (ver GoodPracticeList.vue en /respuestas).
 */
import FlowStatusChip from '~/components/dashboard/flow/FlowStatusChip.vue'
import FlowTransitions from '~/components/dashboard/flow/FlowTransitions.vue'
import FlowComments from '~/components/dashboard/flow/FlowComments.vue'
import { useDates } from '~/composables/useDates.js'

const pkg = defineModel({ type: Object, required: true })

const { formatDate } = useDates()

const institution = computed(
  () => pkg.value.survey_full?.institution_full || {})

const period = computed(
  () => pkg.value.survey_full?.period_full?.year
    || pkg.value.survey_full?.period)

const practices = computed(() => pkg.value.good_practices || [])

// El motor entrega el nuevo status en flowEvent.to_status.
function onTransitioned(flowEvent) {
  pkg.value.status = flowEvent.to_status
}
</script>

<template>
  <v-card variant="flat">
    <!-- Cabecera ─────────────────────────────────────────────────────── -->
    <v-card-title class="d-flex align-center flex-wrap ga-2">
      <v-card
        v-if="pkg.survey_full"
        class="px-3 py-1"
        color="blue"
        variant="tonal"
      >
        {{ institution.name }}
        <span v-if="institution.acronym" class="text-caption ml-1">
          ({{ institution.acronym }})
        </span>
      </v-card>
      <v-card class="px-3 py-1" color="indigo" variant="tonal">
        {{ period }}
      </v-card>
      <v-card
        v-if="pkg.sent_at"
        class="px-3 py-1"
        color="green"
        variant="tonal"
      >
        Enviado el {{ formatDate(pkg.sent_at) }}
      </v-card>
      <v-spacer />
      <FlowStatusChip :status="pkg.status" />
    </v-card-title>

    <!-- Transiciones de la revisora ──────────────────────────────────── -->
    <v-card-text v-if="pkg.id" class="py-2">
      <FlowTransitions
        app-label="example"
        model-name="goodpracticepackage"
        :pk="pkg.id"
        @transitioned="onTransitioned"
      />
    </v-card-text>

    <!-- Prácticas (solo lectura) ─────────────────────────────────────── -->
    <v-card-text v-if="practices.length" class="py-1">
      <div class="text-subtitle-2 mb-1">Buenas prácticas del paquete</div>
      <v-list density="compact">
        <v-list-item
          v-for="p in practices"
          :key="p.id"
          :title="p.name || 'Sin nombre'"
        >
          <template #append>
            <FlowStatusChip :status="p.status" size="small" />
          </template>
        </v-list-item>
      </v-list>
    </v-card-text>

    <!-- Comentarios del paquete ──────────────────────────────────────── -->
    <v-card-text v-if="pkg.id">
      <v-divider class="mb-3" />
      <div class="text-subtitle-2 mb-1">Comentarios del paquete</div>
      <FlowComments
        app-label="example"
        model-name="goodpracticepackage"
        :pk="pkg.id"
      />
    </v-card-text>
  </v-card>
</template>
