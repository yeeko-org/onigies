export function useRules() {
  const rules = {
    required: (v) => !!v || 'Este campo es requerido',
    has_content: v => !!v.length || 'Debes seleccionar al menos una opción',
  }

  return {
    rules,
  }
}