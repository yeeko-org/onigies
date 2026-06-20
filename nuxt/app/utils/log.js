// Logging de diagnóstico solo en desarrollo. En producción son no-ops:
// `import.meta.dev` es una constante que el bundler reemplaza por `false`,
// así que estas llamadas se eliminan por tree-shaking en el build.
// Auto-importadas por Nuxt (carpeta `utils/`): se usan sin import.

export const devWarn = (...args) => {
  if (import.meta.dev) console.warn(...args)
}

export const devLog = (...args) => {
  if (import.meta.dev) console.log(...args)
}