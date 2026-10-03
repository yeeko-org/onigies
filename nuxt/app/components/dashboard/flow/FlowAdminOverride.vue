<script setup>
/**
 * Válvula de admin del flujo (adr-0023, task-190): botón de ícono junto al
 * chip de status + diálogo propio para llevar un hijo o nieto a un status
 * que la revisión establece, fuera de `next_statuses`. Solo existe para
 * `authStore.is_admin` y con raíz; con la raíz fuera del lado de la revisión
 * el botón se ve bloqueado con el motivo en el tooltip, no se oculta.
 *
 * No es un ítem de FlowTransitionMenu a propósito: el menú lista el flujo
 * legal, y la válvula ahí parecería una opción equivalente.
 */
import { useFlowAdminOverride } from '~/composables/useFlowAdminOverride.js'
import FlowStatusChip from '~/components/dashboard/flow/FlowStatusChip.vue'
import FlowTimeline from '~/components/dashboard/flow/FlowTimeline.vue'

const props = defineProps({
  appLabel:  { type: String, required: true },
  modelName: { type: String, required: true },
  // Raíz del flujo (envío o eje): gobierna si hay turno de revisión.
  root:      { type: [Object, Function], required: true },
  // Sigue al chip vecino.
  size:      { type: String, default: 'small' },
})

const emit = defineEmits(['transitioned'])

const record = defineModel({ type: Object, required: true })

const {
  root, available, rootBlocked, targets,
  dialog, target, comment, sending, canSubmit,
  open, close, submit,
} = useFlowAdminOverride(
  record, () => props.appLabel, () => props.modelName, {
    root: () => toValue(props.root),
    onTransitioned: (ev) => emit('transitioned', ev),
  })

const ROOT_LABELS = {
  goodpractice: 'Envío de Buenas Prácticas',
  generalgroupresponse: 'Envío de preguntas generales',
}
const resolvedRootLabel = computed(() => {
  if (ROOT_LABELS[props.modelName]) return ROOT_LABELS[props.modelName]
  const axisName = root.value?.axis_full?.name
  return axisName ? `Eje ${axisName}` : ''
})

const BUTTON_LABEL = 'Cambio administrativo de estatus'

const events = computed(() => record.value?.flow_events || [])

// El error del motivo se muestra al perder el foco o al intentar aplicar,
// no mientras se escribe.
const commentTouched = ref(false)
const commentError = computed(() => commentTouched.value
  && !comment.value.trim() ? 'Escribe el motivo del cambio.' : '')
watch(dialog, (isOpen) => { if (isOpen) commentTouched.value = false })

const radiosRef = ref(null)
function focusRadios() {
  radiosRef.value?.$el
    ?.querySelector('input[type="radio"]:not(:disabled)')?.focus()
}

function onApply() {
  commentTouched.value = true
  return submit()
}
</script>

<template>
  <template v-if="available">
    <!-- Bloqueado: aria-disabled en vez de disabled, para que el tooltip
         con el motivo siga alcanzable por puntero, teclado y lector. -->
    <span
      v-if="rootBlocked.length"
      class="d-inline-flex"
      data-testid="flow-admin-override-blocked"
    >
      <v-btn
        icon
        variant="text"
        :size="size"
        density="comfortable"
        color="grey-lighten-1"
        aria-disabled="true"
        :aria-label="`${BUTTON_LABEL}: ${rootBlocked[0]}`"
        style="cursor: not-allowed;"
      >
        <v-icon>admin_panel_settings</v-icon>
      </v-btn>
      <v-tooltip activator="parent" location="top" max-width="320">
        {{ rootBlocked[0] }}
      </v-tooltip>
    </span>

    <span v-else class="d-inline-flex">
      <v-btn
        icon
        variant="text"
        :size="size"
        density="comfortable"
        color="grey-darken-1"
        :aria-label="BUTTON_LABEL"
        data-testid="flow-admin-override"
        @click="open"
      >
        <v-icon>admin_panel_settings</v-icon>
      </v-btn>
      <v-tooltip activator="parent" location="top">
        {{ BUTTON_LABEL }}
      </v-tooltip>
    </span>

    <v-dialog
      v-model="dialog"
      max-width="560"
      :persistent="sending"
      scrollable
      @after-enter="focusRadios"
    >
      <v-card data-testid="flow-admin-override-dialog">
        <v-card-title class="d-flex align-center">
          <v-icon start>admin_panel_settings</v-icon>
          Cambio administrativo de estatus
        </v-card-title>
        <v-card-text>
          <v-alert
            type="warning"
            variant="tonal"
            density="comfortable"
            role="note"
            class="mb-4"
          >
            Este cambio salta las reglas del flujo de validación y no se
            recomienda. Úsalo solo para corregir un error o destrabar un caso
            excepcional; en cualquier otra situación, utiliza las acciones
            habituales del menú de estatus.
          </v-alert>

          <div class="text-body-2 d-flex align-center flex-wrap ga-2 mb-2">
            <span>Estatus actual:</span>
            <FlowStatusChip :status="record.status" size="small" />
          </div>
          <div class="text-body-2 d-flex align-center flex-wrap ga-2 mb-4">
            <span>Pertenece a:</span>
            <span v-if="resolvedRootLabel">{{ resolvedRootLabel }}</span>
            <FlowStatusChip
              :status="root?.status"
              size="x-small"
              variant="tonal"
            />
          </div>

          <!-- Los destinos legales (next_statuses) no salen aquí: van por
               el menú de estatus, que deja el evento como transición
               normal. -->
          <v-alert
            v-if="!targets.length"
            type="info"
            variant="tonal"
            density="comfortable"
            class="mb-4"
            data-testid="flow-admin-override-empty"
          >
            No hay cambios administrativos posibles desde este estatus; los
            cambios disponibles están en el menú de estatus.
          </v-alert>
          <v-radio-group
            v-else
            ref="radiosRef"
            v-model="target"
            label="Nuevo estatus *"
            hide-details
            class="mb-4"
          >
            <v-radio
              v-for="t in targets"
              :key="t.name"
              :value="t.name"
            >
              <template #label>
                <div class="d-flex align-start ga-2 py-1">
                  <v-icon :color="t.color || 'primary'" size="20" class="mt-1">
                    {{ t.icon || 'trip_origin' }}
                  </v-icon>
                  <div>
                    <div class="font-weight-bold">
                      {{ t.public_name }}
                    </div>
                    <div
                      v-if="t.description"
                      class="text-caption text-medium-emphasis"
                    >
                      {{ t.description }}
                    </div>
                  </div>
                </div>
              </template>
            </v-radio>
          </v-radio-group>

          <!-- Mismo markup que la caja de comentario de ConfirmActionDialog -->
          <v-card variant="tonal" color="grey">
            <v-card-text class="py-3">
              <div
                id="flow-admin-override-guide"
                class="text-body-2 text-medium-emphasis mb-2"
              >
                <v-chip
                  color="warning"
                  size="x-small"
                  label
                  class="mr-1 text-uppercase font-weight-bold"
                >
                  Obligatorio
                </v-chip>
                Explica el motivo del cambio. Quedará registrado en el
                historial como justificación y lo podrán leer la institución y
                el equipo de revisión.
              </div>
              <v-textarea
                v-model="comment"
                label="Motivo del cambio *"
                variant="outlined"
                rows="3"
                auto-grow
                aria-describedby="flow-admin-override-guide"
                :error-messages="commentError"
                :hide-details="!commentError"
                @blur="commentTouched = true"
              />
            </v-card-text>
          </v-card>

          <v-expansion-panels v-if="events.length" class="mt-3">
            <v-expansion-panel>
              <v-expansion-panel-title class="text-body-2">
                <v-icon start size="18">history</v-icon>
                Historial de comentarios y cambios
                <v-chip size="x-small" class="ml-2">
                  {{ events.length }}
                </v-chip>
              </v-expansion-panel-title>
              <v-expansion-panel-text>
                <FlowTimeline :events="events" />
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-card-text>
        <v-card-actions class="mx-2">
          <v-btn variant="outlined" :disabled="sending" @click="close">
            Cancelar
          </v-btn>
          <v-spacer />
          <v-btn
            color="warning"
            variant="flat"
            prepend-icon="admin_panel_settings"
            :loading="sending"
            :disabled="!canSubmit"
            data-testid="flow-admin-override-apply"
            @click="onApply"
          >
            Aplicar cambio administrativo
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
</template>
