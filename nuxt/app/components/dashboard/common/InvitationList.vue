<script setup>
import { useAuthStore } from '~/store/auth.js'
import { useDashboardStore } from '~/store/dash.js'
import { useApiError } from '~/composables/useApiError.js'
import { INVITATION_PERMISSIONS } from '~/composables/usePermissions.js'
import InvitationRow from "~/components/dashboard/ies/institution/InvitationRow.vue"
import DialogDelete from "~/components/dashboard/common/dialog/DialogDelete.vue"

const props = defineProps({
  invitations: {
    type: Array,
    default: () => [],
  },
  institutionId: {
    type: [Number, String],
  },
  // staff_mode: gestiona invitaciones globales de staff (sin institución).
  staff_mode: {
    type: Boolean,
    default: false,
  },
})

const authStore = useAuthStore()
const dashStore = useDashboardStore()
const { notifyApiError } = useApiError()

const NAME_FIELDS = [
  { key: 'first_name', label: 'Nombre(s)' },
  { key: 'last_name',  label: 'Apellidos' },
]

// Las invitaciones que se registraron (used_at) siempre tienen user
// asociado, así que en la práctica los dos primeros filtros son disjuntos.
const FILTER_OPTIONS = [
  { value: 'pending', label: 'Pendientes', match: i => !i.used_at },
  { value: 'linked',  label: 'Vinculadas', match: i => !!i.user    },
  { value: 'all',     label: 'Todas',      match: () => true       },
]

// Estado inicial del formulario. Para resetear:
const INITIAL_FORM = {
  email: '',
  first_name: '',
  last_name: '',
  reviewer: false,
  is_staff: false,
  is_superuser: false,
}

const form_data = reactive({ ...INITIAL_FORM })
const local_invitations = ref([])
const filter = ref('pending')
const loading = ref(false)
const loading_list = ref(false)
const dialog_create = ref(false)
const dialog_delete = ref(false)
const delete_target = ref(null)
const create_form = ref(null)

const counts = computed(() => {
  const acc = { pending: 0, linked: 0, all: local_invitations.value.length }
  for (const i of local_invitations.value) {
    if (!i.used_at) acc.pending++
    if (i.user) acc.linked++
  }
  return acc
})

const filtered_invitations = computed(() => {
  const opt = FILTER_OPTIONS.find(o => o.value === filter.value)
  return opt
    ? local_invitations.value.filter(opt.match)
    : local_invitations.value
})

const email_required_rule = v => !!v || 'El email es obligatorio'
const email_format_rule = v =>
  !v || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'Email inválido'

const email_rules = computed(() =>
  props.staff_mode
    ? [email_required_rule, email_format_rule]
    : [email_format_rule]
)

const table_colspan = computed(() => props.staff_mode ? 8 : 7)

async function loadStaffInvitations() {
  loading_list.value = true
  try {
    const data = await authStore.listInvitations({ hide_institution: true })
    local_invitations.value = data?.results || data || []
  } finally {
    loading_list.value = false
  }
}

onMounted(() => {
  if (props.staff_mode) {
    loadStaffInvitations()
  } else {
    local_invitations.value = [...props.invitations]
  }
})

function openDelete(inv) {
  delete_target.value = inv
  dialog_delete.value = true
}

// El payload depende del modo:
// - staff_mode: todos los campos del formulario
// - institución: institution + email opcional
function buildPayload() {
  if (props.staff_mode) {
    return {
      email: form_data.email,
      first_name: form_data.first_name,
      last_name: form_data.last_name,
      reviewer: form_data.reviewer,
      is_staff: form_data.is_staff,
      is_superuser: form_data.is_superuser,
    }
  }
  const payload = { institution: props.institutionId }
  if (form_data.email) payload.email = form_data.email
  return payload
}

async function createInvitation() {
  const { valid } = await create_form.value.validate()
  if (!valid) return
  loading.value = true
  try {
    const created = await authStore.createInvitation(buildPayload())
    local_invitations.value.push(created)
    dialog_create.value = false
    Object.assign(form_data, INITIAL_FORM)
    create_form.value.resetValidation()
    dashStore.showSnackbar('Invitación creada')
  } catch (err) {
    notifyApiError(err, 'No se pudo crear la invitación')
  } finally {
    loading.value = false
  }
}

async function deleteInvitation() {
  if (!delete_target.value) return
  loading.value = true
  try {
    await authStore.deleteInvitation(delete_target.value.key)
    const idx = local_invitations.value.findIndex(
      i => i.key === delete_target.value.key
    )
    if (idx !== -1) local_invitations.value.splice(idx, 1)
    dialog_delete.value = false
    delete_target.value = null
    dashStore.showSnackbar('Invitación eliminada')
  } catch (err) {
    notifyApiError(err, 'No se pudo eliminar la invitación')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-card flat>
    <v-card-title class="d-flex justify-space-between align-center flex-wrap ga-2">
      Invitaciones
      <v-btn-toggle
        v-model="filter"
        density="compact"
        mandatory
        color="primary"
        variant="outlined"
        class="ml-4"
      >
        <v-btn
          v-for="opt in FILTER_OPTIONS"
          :key="opt.value"
          :value="opt.value"
          size="small"
        >
          {{ opt.label }} ({{ counts[opt.value] }})
        </v-btn>
      </v-btn-toggle>
      <v-spacer />
      <v-btn
        size="small"
        variant="outlined"
        color="primary"
        @click="dialog_create = true"
      >
        Agregar invitación
      </v-btn>
    </v-card-title>

    <v-table density="compact">
      <thead>
        <tr>
          <th>Email / Persona</th>
          <th>Creación</th>
          <th>Vista</th>
          <th>Usada</th>
          <th class="text-center">Enviada</th>
          <th class="text-center">URL</th>
          <th v-if="staff_mode" class="text-center">Permisos</th>
          <th class="text-center">Eliminar</th>
        </tr>
      </thead>
      <tbody>
        <InvitationRow
          v-for="inv in filtered_invitations"
          :key="inv.key"
          :invitation="inv"
          :loading="loading"
          :staff_mode="staff_mode"
          @delete="openDelete"
        />
        <tr v-if="loading_list">
          <td :colspan="table_colspan" class="text-center py-3">
            <v-progress-circular indeterminate size="20" width="2" />
          </td>
        </tr>
        <tr v-else-if="!filtered_invitations.length">
          <td :colspan="table_colspan" class="text-center text-grey py-3">
            {{ local_invitations.length
              ? 'Sin invitaciones en este filtro'
              : 'Sin invitaciones' }}
          </td>
        </tr>
      </tbody>
    </v-table>

    <!-- Dialog crear -->
    <v-dialog v-model="dialog_create" max-width="560">
      <v-card>
        <v-card-title>Nueva invitación</v-card-title>
        <v-card-text>
          <v-alert
            type="info"
            border="start"
            variant="outlined"
            class="mb-4"
          >
            <template v-if="!staff_mode">
              Si se proporciona un email, se enviará una invitación automática
              al correo.
              <br/>
              <br/>
              De lo contrario, se deberá compartir la URL de invitación
              manualmente.
            </template>
            <template v-else>
              Se enviará una invitación al correo indicado.
              La persona podrá registrarse con los permisos seleccionados.
            </template>
          </v-alert>
          <v-form ref="create_form">
            <v-text-field
              v-model="form_data.email"
              :label="staff_mode ? 'Email' : 'Email (opcional)'"
              :rules="email_rules"
              clearable
            />

            <template v-if="staff_mode">
              <v-row dense>
                <v-col
                  v-for="field in NAME_FIELDS"
                  :key="field.key"
                  cols="12"
                  sm="6"
                >
                  <v-text-field
                    v-model="form_data[field.key]"
                    :label="field.label"
                  />
                </v-col>
              </v-row>

              <div class="text-subtitle-2 mt-2 mb-1">Permisos</div>
              <v-row dense>
                <v-col
                  v-for="perm in INVITATION_PERMISSIONS"
                  :key="perm.key"
                  cols="12"
                >
                  <v-checkbox
                    v-model="form_data[perm.key]"
                    density="compact"
                    hide-details
                  >
                    <template v-slot:label>
                      <span>{{ perm.label }}</span>
                      <span
                        v-if="perm.description"
                        class="text-body-2 text-grey ml-3"
                      >
                        {{ perm.description }}
                      </span>
                    </template>
                  </v-checkbox>
                </v-col>
              </v-row>
            </template>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="dialog_create = false">Cancelar</v-btn>
          <v-btn
            color="primary"
            :loading="loading"
            @click="createInvitation"
          >Crear</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog eliminar -->
    <DialogDelete
      v-model="dialog_delete"
      title="Eliminar invitación"
      :loading="loading"
      @confirm-delete="deleteInvitation"
    >
      ¿Eliminar la invitación
      <strong>{{ delete_target?.email || 'sin email' }}</strong>?
    </DialogDelete>
  </v-card>
</template>

<style scoped>
</style>