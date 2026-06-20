import { shallowRef } from 'vue'

// Registro perezoso de los componentes del dashboard, por ruta glob-relativa.
const dashboardModules = import.meta.glob('../components/dashboard/**/*.vue')

const GENERIC = '../components/dashboard/common/generic'

const FALLBACKS = {
  Header: `${GENERIC}/HeaderGeneric.vue`,
  Sheet: `${GENERIC}/SheetCommon.vue`,
  Edit: `${GENERIC}/EditGeneric.vue`,
  Card: `${GENERIC}/CardGeneric.vue`,
  EditSimple: null,
}

// Resuelve por convención de nombre el componente
// {ModelName}{suffix}.vue de una colección; si no existe, usa el genérico.
export function useDynamicComponent(collectionData, suffix) {
  const comp = shallowRef('')
  const { app_label, snake_name, model_name } = collectionData
  const key = `../components/dashboard/${app_label}/${snake_name}` +
    `/${model_name}${suffix}.vue`
  const fallbackKey = FALLBACKS[suffix]
  const loader = dashboardModules[key] ||
    (fallbackKey ? dashboardModules[fallbackKey] : null)
  if (!dashboardModules[key] && import.meta.dev && fallbackKey)
    console.warn(`[useDynamicComponent] sin ${key}; se usa el genérico`)
  if (loader)
    loader().then(m => { comp.value = m.default })
  return comp
}
