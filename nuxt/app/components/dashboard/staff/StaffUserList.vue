<script setup>
import { useAuthStore } from '~/store/auth.js'
import { useDashboardStore } from '~/store/dash.js'
import { useApiError } from '~/composables/useApiError.js'
import { useDates } from '~/composables/useDates.js'
import { USER_PERMISSIONS } from '~/composables/usePermissions.js'

const authStore = useAuthStore()
const dashStore = useDashboardStore()
const { notifyApiError } = useApiError()
const { formatDate } = useDates()

const PERMISSION_KEYS = USER_PERMISSIONS.map(p => p.key)

const users = ref([])
const loading_list = ref(false)

// Edición: una fila a la vez. `draft` es la copia editable de los flags
// del usuario en edición; al guardar se calcula el diff vs. el original
// y solo eso se envía en el PATCH.
const editing_id = ref(null)
const draft = reactive({})
const saving = ref(false)

async function loadUsers() {
  loading_list.value = true
  try {
    const data = await authStore.listUsers()
    users.value = data?.results || data || []
  } finally {
    loading_list.value = false
  }
}

function enterEdit(user) {
  editing_id.value = user.id
  for (const k of PERMISSION_KEYS) {
    draft[k] = !!user[k]
  }
}

function cancelEdit() {
  editing_id.value = null
  for (const k of PERMISSION_KEYS) delete draft[k]
}

function buildDiffPayload(user) {
  const payload = {}
  for (const k of PERMISSION_KEYS) {
    if (draft[k] !== !!user[k]) payload[k] = draft[k]
  }
  return payload
}

async function saveEdit() {
  const user = users.value.find(u => u.id === editing_id.value)
  if (!user) return
  const payload = buildDiffPayload(user)
  if (!Object.keys(payload).length) {
    cancelEdit()
    return
  }
  saving.value = true
  try {
    const updated = await authStore.updateUserPermissions(user.id, payload)
    Object.assign(user, updated)
    dashStore.showSnackbar('Cambios guardados')
    cancelEdit()
  } catch (err) {
    notifyApiError(err, 'No se pudieron guardar los cambios')
  } finally {
    saving.value = false
  }
}

function isEditingThis(userId) {
  return editing_id.value === userId
}

function isAnotherEditing(userId) {
  return editing_id.value !== null && editing_id.value !== userId
}

onMounted(loadUsers)
</script>

<template>
  <v-card flat>
    <v-card-title class="d-flex justify-space-between align-center">
      Personas usuarias
      <v-btn
        size="small"
        variant="text"
        icon="refresh"
        :loading="loading_list"
        :disabled="editing_id !== null"
        v-tooltip:bottom="'Recargar lista'"
        @click="loadUsers"
      />
    </v-card-title>

    <v-table density="compact">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Email</th>
          <th>Último login</th>
          <th
            v-for="perm in USER_PERMISSIONS"
            :key="perm.key"
            class="text-center"
          >
            <span v-tooltip:bottom="perm.description">{{ perm.label }}</span>
          </th>
          <th class="text-center">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="user in users"
          :key="user.id"
          :class="{ 'text-medium-emphasis': !user.is_active }"
        >
          <td>{{ user.fullname || '—' }}</td>
          <td>{{ user.email || user.username }}</td>
          <td>{{ formatDate(user.last_login) }}</td>
          <td
            v-for="perm in USER_PERMISSIONS"
            :key="perm.key"
            class="text-center"
          >
            <v-checkbox
              v-if="isEditingThis(user.id)"
              v-model="draft[perm.key]"
              density="compact"
              hide-details
              color="success"
              class="d-inline-flex justify-center"
              v-tooltip:bottom="perm.description"
            />
            <v-icon
              v-else-if="user[perm.key]"
              color="success"
              icon="done"
              v-tooltip:bottom="perm.description"
            />
            <v-icon
              v-else
              color="grey-lighten-2"
              icon="remove"
              v-tooltip:bottom="`Sin permiso: ${perm.label}`"
            />
          </td>
          <td class="text-center">
            <template v-if="isEditingThis(user.id)">
              <v-btn
                icon="save"
                size="small"
                variant="text"
                color="success"
                :loading="saving"
                v-tooltip:bottom="'Guardar cambios'"
                @click="saveEdit"
              />
              <v-btn
                icon="close"
                size="small"
                variant="text"
                :disabled="saving"
                v-tooltip:bottom="'Cancelar'"
                @click="cancelEdit"
              />
            </template>
            <v-btn
              v-else
              icon="edit"
              size="x-small"
              variant="text"
              :disabled="isAnotherEditing(user.id)"
              v-tooltip:bottom="isAnotherEditing(user.id)
                ? 'Otra fila está siendo editada'
                : 'Editar permisos'"
              @click="enterEdit(user)"
            />
          </td>
        </tr>
        <tr v-if="loading_list">
          <td :colspan="4 + USER_PERMISSIONS.length" class="text-center py-3">
            <v-progress-circular indeterminate size="20" width="2" />
          </td>
        </tr>
        <tr v-else-if="!users.length">
          <td
            :colspan="4 + USER_PERMISSIONS.length"
            class="text-center text-grey py-3"
          >
            Sin personas usuarias
          </td>
        </tr>
      </tbody>
    </v-table>
  </v-card>
</template>

<style scoped>
</style>