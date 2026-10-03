import { defineConfig } from 'vitest/config'
import { realpathSync } from 'node:fs'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

// `pinia` arrives through @pinia/nuxt, not as a direct dependency, so pnpm's
// isolated layout leaves the bare specifier unresolvable outside Nuxt. Its
// copy is the sibling of @pinia/nuxt inside the .pnpm store (neither package
// exports package.json, so require.resolve cannot reach it).
const root = fileURLToPath(new URL('.', import.meta.url))
const piniaNuxt = realpathSync(resolve(root, 'node_modules/@pinia/nuxt'))
const piniaDir = resolve(piniaNuxt, '../../pinia')

export default defineConfig({
  resolve: {
    alias: [
      { find: '~', replacement: resolve(root, 'app') },
      { find: /^pinia$/, replacement: piniaDir },
    ],
  },
  test: {
    include: ['tests/unit/**/*.test.js'],
  },
})
