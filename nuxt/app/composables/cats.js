import { devWarn } from "~/utils/log.js";

/** @typedef {import('~/types/collection.js').CollectionData
 *   } CollectionData */
/** @typedef {import('~/types/collection.js').FilterGroup} FilterGroup */

/**
 * Enriches the raw `/catalogs/all/` payload into the dashboard schemas.
 * @param {Object} data Raw payload from `/catalogs/all/`.
 * @returns {import('~/types/collection.js').Schemas}
 */
export function calculateSchemas(data) {
  const status_filters = (data.status_groups || []).reduce((obj, sg) => {
    obj[sg.collection] = sg
    return obj
  }, {})
  let filter_groups = data.filter_groups.map(fg => {
    let new_fg =  {...fg, ...fg.addl_config}
    const cat_group = new_fg.category_group || new_fg.special_group
    if (cat_group)
      new_fg.category_groups = data[cat_group] || []
    return new_fg
  })
  const filters_dict = filter_groups.reduce((obj, fg) => {
    obj[fg.key_name] = fg
    return obj
  }, {})
  let collections = data.collections.map(
      (/** @type {CollectionData} */ coll) => {
    const valid_relations = ['one_to_many', 'many_to_many']
    coll.child_relation_fields = coll.fields.filter(field => {
      return valid_relations.includes(field.relation_type)
    })
    // pk, name_field, has y status_groups vienen del payload (ps_schema).
    const other_fields = Object.keys(coll.has).concat(
      [coll.pk, coll.name_field])
    coll.other_fields = coll.fields.filter(f =>
      !other_fields.includes(f.name) && f.relation_type === 'simple')

    const all_filters = coll.all_filters || []

    let available_sorts = [
      {
        title: "Más recientes",
        value: "-id"
      },
      {
        title: "Más antiguos",
        value: "id"
      },
    ]

    let collection_filters = all_filters.reduce((arr, filter) => {
      if (!filter.filter_name){
        arr.push({...filter, order: 12, is_custom: true})
        return arr
      }
      const filter_data = filters_dict[filter.filter_name]
      if (!filter_data){
        devWarn("cats: sin datos de filtro para", filter.filter_name)
        return arr
      }
      const new_filter = {...filter_data, ...filter}
      arr.push(new_filter)
      return arr
    }, [])
    coll.is_category = coll.level.includes('category_')
    if (coll.is_category){
      const fg = filter_groups.find(fg => fg[coll.level] === coll.snake_name)
      // const fg = filters_dict[coll.snake_name]
      if (fg){
        coll.filter_group = fg
        const short_level = coll.level.replace('category_', '')
        const new_filter_group = {
          ...fg,
          short_name: `${fg.short_prev} ${fg.name}`,
          name: `${fg.prev} ${fg.name}`,
          original_name: fg.name,
          forced_level: short_level,
          order: 1,
          hide_in_filter: false,
        }
        collection_filters.push(new_filter_group)
      }
    }

    if (coll.name_field)
      available_sorts.push({
        title: "Nombre / Título",
        value: coll.name_field
      })
    if (coll.has.order)
      available_sorts.push({
        title: "Orden",
        value: "order"
      })
    collection_filters = collection_filters.sort((a, b) => a.order - b.order)

    coll.collection_filters = collection_filters
    coll.available_sorts = available_sorts
    return {...coll.cat_params, ...coll}
  })

  let collections_dict = collections.reduce((obj, coll) => {
    obj[coll.snake_name] = coll
    // obj[coll.model_name] = coll
    return obj
  }, {})
  return {
    "collections": collections,
    "collections_dict": collections_dict,
    "filter_groups": filter_groups,
    "levels": data.levels,
    "filters_dict": filters_dict,
    "status_filters": status_filters,
  }
}
