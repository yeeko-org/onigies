import { defineConfig } from 'vitest/config'
import { fileURLToPath } from 'node:url'

// Vitest solo para lógica pura; los e2e/*.test.ts son de Playwright y no
// deben entrar en este runner.
export default defineConfig({
  resolve: {
    alias: {
      '~': fileURLToPath(new URL('./app', import.meta.url)),
    },
  },
  test: {
    include: ['tests/unit/**/*.test.js'],
  },
})
