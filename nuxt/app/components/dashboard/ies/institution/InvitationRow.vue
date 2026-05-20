<script setup>
import { useDashboardStore } from '~/store/dash.js'
import { useDates } from '~/composables/useDates.js'
import { INVITATION_PERMISSIONS } from '~/composables/usePermissions.js'

const props = defineProps({
  invitation: { type: Object, required: true },
  loading: { type: Boolean, default: false },
  staff_mode: { type: Boolean, default: false },
})

const emit = defineEmits(['delete'])

const dashStore = useDashboardStore()
const { formatDate } = useDates()

const activePermissions = computed(() =>
  INVITATION_PERMISSIONS.filter(p => !!props.invitation[p.key])
)

const EMAIL_SENT_MAP = {
  true:  {
    color: 'success',
    icon: 'check',
    tooltip: 'La invitación fue enviada al correo'
  },
  false: {
    color: 'error',
    icon: 'warning',
    tooltip: 'Hubo un error al enviar la invitación al correo'
  },
}

const COPY_STATE_MAP = {
  true:  { icon: 'check',        color: 'success'  },
  false: { icon: 'content_copy', color: undefined  },
}

const hasEmail = computed(() => !!props.invitation.email)
const isUsed   = computed(() => !!props.invitation.used_at)
const emailSent = computed(() => !!props.invitation.email_sent)

const registeredUser = computed(() => props.invitation.user || null)
const invitedAsDifferent = computed(
  () => registeredUser.value
    && props.invitation.email
    && props.invitation.email !== registeredUser.value.email
)

const emailStatus = computed(() => EMAIL_SENT_MAP[String(emailSent.value)])

const copied = ref(false)
const copyState = computed(() => COPY_STATE_MAP[String(copied.value)])

// No se permite eliminar si:
// - la invitación ya fue usada (hay un usuario real vinculado)
// - el correo ya fue enviado (la persona puede estar por usarla)
const canDelete = computed(() => !isUsed.value && !(hasEmail.value && emailSent.value))

const deleteTooltip = computed(() => {
  if (isUsed.value) return 'No se puede eliminar: ya fue utilizada'
  if (hasEmail.value && emailSent.value)
    return 'No se puede eliminar: el correo ya fue enviado'
  return 'Eliminar invitación'
})

async function copyUrl() {
  await navigator.clipboard.writeText(props.invitation.destination_url)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
  dashStore.showSnackbar('URL copiada al portapapeles')
}
</script>

<template>
  <tr>
    <td>
      <template v-if="registeredUser">
        <div>{{ registeredUser.full_name }}</div>
        <div class="text-caption text-grey">{{ registeredUser.email }}</div>
        <div
          v-if="invitedAsDifferent"
          class="text-caption text-grey font-italic"
        >
          Invitada como: {{ invitation.email }}
        </div>
      </template>
      <span v-else-if="hasEmail">{{ invitation.email }}</span>
      <span v-else class="text-grey">Sin email</span>
    </td>
    <td>{{ formatDate(invitation.created_at) }}</td>
    <td>
      <v-chip
        v-if="invitation.viewed_at"
        color="success"
        size="x-small"
        label
      >
        {{ formatDate(invitation.viewed_at) }}
      </v-chip>
      <span v-else class="text-grey">—</span>
    </td>
    <td>
      <v-chip
        v-if="isUsed"
        color="success"
        size="x-small"
        label
      >
        {{ formatDate(invitation.used_at) }}
      </v-chip>
      <span v-else class="text-grey">—</span>
    </td>
    <td class="text-center">
      <template v-if="hasEmail">
        <v-icon :color="emailStatus.color" :icon="emailStatus.icon">
          <v-tooltip activator="parent" location="bottom">
            {{ emailStatus.tooltip }}
          </v-tooltip>
        </v-icon>
      </template>
      <span v-else class="text-grey">—</span>
    </td>
    <td class="text-center">
      <v-btn
        :icon="copyState.icon"
        size="x-small"
        variant="text"
        :color="copyState.color"
        v-tooltip:bottom="'Copiar URL de invitación'"
        @click="copyUrl"
      />
    </td>
    <td v-if="staff_mode" class="text-center">
      <template v-if="activePermissions.length">
        <v-chip
          v-for="p in activePermissions"
          :key="p.key"
          :color="p.color"
          size="x-small"
          label
          class="mr-1"
          v-tooltip:bottom="p.description"
        >
          {{ p.label }}
        </v-chip>
      </template>
      <span v-else class="text-grey">—</span>
    </td>
    <td class="text-center">
      <v-btn
        icon="delete"
        size="x-small"
        variant="text"
        color="error"
        :disabled="!canDelete || loading"
        v-tooltip:bottom="deleteTooltip"
        @click="emit('delete', invitation)"
      />
    </td>
  </tr>
</template>

<style scoped>
</style>