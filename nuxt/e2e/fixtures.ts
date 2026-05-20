import { test as base } from '@playwright/test'
import { installMocks } from './mocks/handlers'

// `test` custom: cada test arranca con el catchAll instalado. Los
// tests luego añaden sus mocks específicos (más prioridad).
export const test = base.extend({
  page: async ({ page }, use) => {
    await installMocks(page)
    await use(page)
  },
})

export { expect } from '@playwright/test'