import {useMainStore} from "~/store/index.js";
import {storeToRefs} from "pinia";
import { devWarn } from "~/utils/log.js";

/** @typedef {import('~/types/collection.js').CollectionData
 *   } CollectionData */

// Campos de archivo que el GET devuelve como URL (o como objeto que la
// envuelve): reenviarlos al guardar provoca un 400 «The submitted data was
// not a file». Solo deben viajar cuando hay un archivo nuevo; el logo, de
// hecho, se sube por su propio endpoint (upload_logo).
const FILE_FIELDS_BY_COLLECTION = {
  institution: ['logo'],
}

function withoutUnchangedFiles(snake_name, element) {
  const file_fields = FILE_FIELDS_BY_COLLECTION[snake_name]
  if (!file_fields) return element
  const clean_element = {...element}
  file_fields.forEach(field_name => {
    if (!(clean_element[field_name] instanceof File))
      delete clean_element[field_name]
  })
  return clean_element
}

/** @param {CollectionData} collection_data */
function final_snake_name(collection_data) {
  const is_category = collection_data.is_category
  const snake_name = collection_data.snake_name
  return { snake_name, is_category }
}

/** @param {CollectionData} collection_data */
export async function saveElement(collection_data, element, error_msg = null) {
  const mainStore = useMainStore()
  const { saveSimple, saveCatalog } = mainStore
  const { snake_name, is_category } = final_snake_name(collection_data)
  const clean_element = withoutUnchangedFiles(snake_name, element)
  if (is_category)
    return await saveCatalog([collection_data, clean_element], error_msg)
  else
    return await saveSimple([snake_name, clean_element], error_msg)
}

/** @param {CollectionData} collection_data */
export async function patchElement(
    collection_data, elem_id, params, error_msg = null) {
  const mainStore = useMainStore()
  const { patchSimple, patchCatalog } = mainStore
  const { snake_name, is_category } = final_snake_name(collection_data)
  if (is_category)
    return await patchCatalog([collection_data, elem_id, params], error_msg)
  else
    return await patchSimple([snake_name, elem_id, params], error_msg)
}

/** @param {CollectionData} collection_data */
export async function deleteElement(collection_data, obj_id, error_msg = null) {
  const mainStore = useMainStore()
  const { deleteSimple, deleteCatalog } = mainStore
  const { snake_name, is_category } = final_snake_name(collection_data)
  if (is_category)
    return await deleteCatalog([collection_data, obj_id], error_msg)
  else
    return await deleteSimple([snake_name, obj_id], error_msg)
}

/** @param {CollectionData} collection_data */
export async function getElement(collection_data, el_id, error_msg = null) {
  const mainStore = useMainStore()
  const { getSimple } = mainStore
  let { snake_name, is_category } = final_snake_name(collection_data)
  if (is_category)
    snake_name = `catalogs/${snake_name}`
  return await getSimple([snake_name, el_id], error_msg)
}

export function useSaveElements() {
  const total_requests = ref(0)
  const resolved_requests = ref(0)
  const save_errors = ref([])
  const participants_dict = ref({})
  const normal_save = ref(true)
  const first_special = ref(false)

  function saveComplex(collection_name, element, copy_id=null) {
    normal_save.value = !copy_id

    return new Promise((resolve, reject) => {
      total_requests.value = 0
      resolved_requests.value = 0
      save_errors.value = []

      const checkFinished = () => {
        if (resolved_requests.value === total_requests.value) {
          // console.log("All requests finished", save_errors.value)
          if (save_errors.value.length > 0) {
            reject(save_errors.value)
          } else {
            resolve()
          }
        }
      }

      const checkInitialFinished = () => {
        if (resolved_requests.value === total_requests.value) {
          first_special.value = false
          saveOneToMany(collection_name, element, checkFinished, copy_id)
        }
      }

      if (copy_id) {
        first_special.value = true
        saveOneToMany(collection_name, element, checkInitialFinished, copy_id)
      }
      else{
        saveOneToMany(collection_name, element, checkFinished)
      }

    })
  }

  function saveOneToMany(snake_name, main_item, onFinished, parent_id=null) {
    const mainStore = useMainStore()
    const { schemas } = storeToRefs(mainStore)
    const { saveSimple } = mainStore

    const main_schema = schemas.value.collections_dict[snake_name]
    const one_to_many_fields = main_schema.fields.filter(
      field => field.relation_type === 'one_to_many')

    one_to_many_fields.forEach(field => {
      // console.log("Processing field", field.name, "of collection", snake_name)
      if (!normal_save.value){
        const is_actor = ['participants', 'interests'].includes(field.name)
        if (first_special.value && !is_actor)
          return
        if (!first_special.value && is_actor)
          return
      }

      if (['involved', "eventlocation", "clicks"].includes(field.name))
        return
      if (field.name.includes('displacement_'))
        return

      const related_collection = schemas.value.collections_dict[
        field.related_snake_name]
      // if (!related_collection) {
      //   console.error('Related collection not found for field', field)
      //   // return
      // }
      const snake_name2 = related_collection.snake_name
      const item_list = main_item[field.name]
      if (!item_list){
        devWarn(`Sin items que guardar en el campo ${field.name}`, main_item)
        return
      }

      item_list.forEach(item => {
        if (item.path && !item.id)
          return
        const new_item = {...item}

        if (!normal_save.value) {
          new_item[snake_name] = parent_id
          new_item.id = null
          if (snake_name2 === 'involved')
            new_item['participant'] = participants_dict.value[item.participant]
        }
        total_requests.value += 2

        saveSimple([snake_name2, new_item]).then(res => {
          if (res.errors) {
            devWarn(`Error al guardar ${snake_name2}:`, res.errors)
            save_errors.value.push({
              field: `${field.name} --> ${snake_name2}`,
              item: new_item,
              errors: res.errors,
            })
          }
          if (first_special.value && field.name === 'participants')
            participants_dict.value[item.id] = res.data?.id

          if (!normal_save.value)
            saveOneToMany(snake_name2, new_item, onFinished, res.data?.id)

          resolved_requests.value += 1
          onFinished()
        })
        if (normal_save.value)
          saveOneToMany(snake_name2, item, onFinished)
        resolved_requests.value += 1
        onFinished()
      })
    })

    if (total_requests.value === 0) {
      onFinished()
    }
  }

  return {
    saveComplex,
    save_errors
  }
}
