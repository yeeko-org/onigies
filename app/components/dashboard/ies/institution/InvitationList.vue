<script setup>
import { useAuthStore } from '~/store/auth.js'

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

const local_invitations = ref([...props.invitations])
const loading = ref(false)
const dialog_create = ref(false)
const dialog_delete = ref(false)
const delete_target = ref(null)
const new_email = ref('')
const copied_key = ref(null)
const create_form = ref(null)

const email_rule = v => !v || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'Email inválido'

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('es-MX', { dateStyle: 'short' })
}

async function copyUrl(inv) {
  await navigator.clipboard.writeText(inv.destination_url)
  copied_key.value = inv.key
  setTimeout(() => { copied_key.value = null }, 2000)
}

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
          <th>Creada</th>
          <th>Vista</th>
          <th>Usada</th>
          <th>URL</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="inv in local_invitations" :key="inv.key">
          <td>{{ inv.email || '—' }}</td>
          <td>{{ formatDate(inv.created_at) }}</td>
          <td>{{ formatDate(inv.viewed_at) }}</td>
          <td>
            <v-chip v-if="inv.used_at" color="success" size="x-small" label>
              {{ formatDate(inv.used_at) }}
            </v-chip>
            <span v-else class="text-grey">—</span>
          </td>
          <td>
            <v-btn
              :icon="copied_key === inv.key ? 'check' : 'content_copy'"
              size="x-small"
              variant="text"
              :color="copied_key === inv.key ? 'success' : undefined"
              @click="copyUrl(inv)"
            />
          </td>
          <td>
            <v-btn
              icon="delete"
              size="x-small"
              variant="text"
              color="error"
              :disabled="!!inv.used_at"
              @click="openDelete(inv)"
            />
          </td>
        </tr>
        <tr v-if="!local_invitations.length">
          <td colspan="6" class="text-center text-grey py-3">Sin invitaciones</td>
        </tr>
      </tbody>
    </v-table>

    <!-- Dialog crear -->
    <v-dialog v-model="dialog_create" max-width="400">
      <v-card>
        <v-card-title>Nueva invitación</v-card-title>
        <v-card-text>
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