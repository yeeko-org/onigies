<script setup>
import { useAuthStore } from '~/store/auth.js'
import { useDashboardStore } from '~/store/dash.js'
import InvitationRow from "~/components/dashboard/ies/institution/InvitationRow.vue";

const props = defineProps({
  invitations: {
    type: Array,
    default: () => [],
  },
  institutionId: {
    type: [Number, String],
    required: true,
  },
})

const authStore = useAuthStore()
const dashStore = useDashboardStore()

const local_invitations = ref([...props.invitations])
const loading = ref(false)
const dialog_create = ref(false)
const dialog_delete = ref(false)
const delete_target = ref(null)
const new_email = ref('')
const create_form = ref(null)

const email_rule = v => !v || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'Email inválido'

function openDelete(inv) {
  delete_target.value = inv
  dialog_delete.value = true
}

async function createInvitation() {
  const { valid } = await create_form.value.validate()
  if (!valid) return
  loading.value = true
  try {
    const payload = { institution: props.institutionId }
    if (new_email.value) payload.email = new_email.value
    const created = await authStore.createInvitation(payload)
    local_invitations.value.push(created)
    dialog_create.value = false
    new_email.value = ''
    create_form.value.reset()
    dashStore.showSnackbar('Invitación creada')
  } finally {
    loading.value = false
  }
}

async function deleteInvitation() {
  if (!delete_target.value) return
  loading.value = true
  try {
    await authStore.deleteInvitation(delete_target.value.key)
    const idx = local_invitations.value.findIndex(i => i.key === delete_target.value.key)
    if (idx !== -1) local_invitations.value.splice(idx, 1)
    dialog_delete.value = false
    delete_target.value = null
    dashStore.showSnackbar('Invitación eliminada')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-card flat>
    <v-card-title class="d-flex justify-space-between align-center">
      Invitaciones
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
          <th>Email</th>
          <th>Creación</th>
          <th>Vista</th>
          <th>Usada</th>
          <th class="text-center">URL</th>
          <th class="text-center">Eliminar</th>
        </tr>
      </thead>
      <tbody>
        <InvitationRow
          v-for="inv in local_invitations"
          :key="inv.key"
          :invitation="inv"
          :loading="loading"
          @delete="openDelete"
        />
        <tr v-if="!local_invitations.length">
          <td colspan="6" class="text-center text-grey py-3">Sin invitaciones</td>
        </tr>
      </tbody>
    </v-table>

    <!-- Dialog crear -->
    <v-dialog v-model="dialog_create" max-width="500">
      <v-card>
        <v-card-title>Nueva invitación</v-card-title>
        <v-card-text>
          <v-alert type="info" border="start" variant="outlined" class="mb-4">
            Si se proporciona un email, se enviará una invitación automática
            al correo.
            <br/>
            <br/>
            De lo contrario, se deberá compartir la URL de invitación manualmente.
          </v-alert>

          <v-form ref="create_form">
            <v-text-field
              v-model="new_email"
              label="Email (opcional)"
              :rules="[email_rule]"
              clearable
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="dialog_create = false">Cancelar</v-btn>
          <v-btn color="primary" :loading="loading" @click="createInvitation">Crear</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog eliminar -->
    <v-dialog v-model="dialog_delete" max-width="400">
      <v-card>
        <v-card-title>Eliminar invitación</v-card-title>
        <v-card-text>
          ¿Eliminar la invitación
          <strong>{{ delete_target?.email || 'sin email' }}</strong>?
          Esta acción no se puede deshacer.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="dialog_delete = false">Cancelar</v-btn>
          <v-btn color="error" :loading="loading" @click="deleteInvitation">Eliminar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<style scoped>
</style>