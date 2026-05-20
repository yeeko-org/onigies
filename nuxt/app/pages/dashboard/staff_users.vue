<script setup>
import { useAuthStore } from '~/store/auth.js'
import { useDashboardStore } from '~/store/dash.js'
import StaffUserList from '~/components/dashboard/staff/StaffUserList.vue'
import InvitationList from '~/components/dashboard/common/InvitationList.vue'

const authStore = useAuthStore()
const dashStore = useDashboardStore()
const router = useRouter()

const active_tab = ref('users')

onMounted(() => {
  if (!authStore.user_onigies?.is_superuser) {
    dashStore.showSnackbar('Acceso denegado')
    router.push('/dashboard')
  }
})
</script>

<template>
  <v-card v-if="authStore.user_onigies?.is_superuser" class="mt-3 w-100">
    <v-tabs v-model="active_tab" color="primary" align-tabs="start">
      <v-tab value="users">Personas usuarias</v-tab>
      <v-tab value="invitations">Invitaciones</v-tab>
    </v-tabs>
    <v-divider />
    <v-window v-model="active_tab">
      <v-window-item value="users">
        <v-card-text>
          <StaffUserList />
        </v-card-text>
      </v-window-item>
      <v-window-item value="invitations">
        <v-card-text>
          <InvitationList staff_mode />
        </v-card-text>
      </v-window-item>
    </v-window>
  </v-card>
</template>

<style scoped>
</style>