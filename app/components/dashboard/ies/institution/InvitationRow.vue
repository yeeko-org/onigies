<script setup>
import { useDashboardStore } from '~/store/dash.js'

const props = defineProps({
  invitation: { type: Object, required: true },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['delete'])

const dashStore = useDashboardStore()

const EMAIL_SENT_MAP = {
  true:  {
    color: 'success',
    icon: 'check',
    label: 'Enviado',
    tooltip: 'La invitación fue enviada al correo'
  },
  false: {
    color: 'error',
    icon: 'warning',
    label: 'No enviado',
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

const emailStatus = computed(() => EMAIL_SENT_MAP[String(emailSent.value)])

const copied = ref(false)
const copyState = computed(() => COPY_STATE_MAP[String(copied.value)])

async function copyUrl() {
  await navigator.clipboard.writeText(props.invitation.destination_url)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
  dashStore.showSnackbar('URL copiada al portapapeles')
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString(
    'es-MX', { dateStyle: 'short' })
}
</script>

<template>
  <tr>
    <td>
      <span v-if="hasEmail">{{ invitation.email }}</span>
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
      <v-btn
        v-if="!hasEmail"
        :icon="copyState.icon"
        size="x-small"
        variant="text"
        :color="copyState.color"
        v-tooltip:bottom="'Copiar URL de invitación'"
        @click="copyUrl"
      />
      <v-chip
        v-else
        :color="emailStatus.color"
        size="small"
        label
        class="ms-2"
      >
        {{ emailStatus.label }}
        <v-icon :icon="emailStatus.icon" size="x-small" class="ms-1" />
        <v-tooltip activator="parent" location="bottom">
          {{ emailStatus.tooltip }}
        </v-tooltip>
      </v-chip>
    </td>
    <td class="text-center">
      <v-btn
        icon="delete"
        size="x-small"
        variant="text"
        color="error"
        :disabled="isUsed || loading || (hasEmail && emailSent)"
        @click="emit('delete', invitation)"
      />
    </td>
  </tr>
</template>

<style scoped>
</style>