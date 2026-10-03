import { createPinia, setActivePinia } from 'pinia'
import { useAuthStore } from '~/store/auth'
import { useFlowStore } from '~/store/flow.js'
import { seedCatalog } from './flow_catalog.js'
import { mainStoreStub } from './main_store_stub.js'

export const USERS = {
  superuser: { id: 1, is_superuser: true },
  staff: { id: 2, is_staff: true },
  reviewer: { id: 3, reviewer: true },
  ies: { id: 4, institution: 10 },
}

/**
 * Pinia nueva por test, con el catálogo del seed y la persona usuaria dada.
 * `users` llena el catálogo de personas que lee `eventSide`.
 */
export function setupFlowStore({ user = null, users = {}, catalog } = {}) {
  setActivePinia(createPinia())
  mainStoreStub.users_by_id = users
  const auth = useAuthStore()
  auth.user_onigies = user
  const flow = useFlowStore()
  flow.byName = catalog || seedCatalog()
  return { flow, auth }
}
