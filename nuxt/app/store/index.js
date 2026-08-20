// import ApiService from "./common";
// import { mande } from 'mande'
import { defineStore } from 'pinia'
import axios from "axios";
import { calculateNewCats, hydrateFilterGroup } from "~/composables/nodes.js";
import { calculateSchemas } from "~/composables/cats.js";
import { calculate_status } from "~/composables/filters.js";
import { devWarn } from "~/utils/log.js";
import { ok, fail } from "~/utils/api.js";
let request = axios.CancelToken.source();

/** @typedef {import('~/types/collection.js').CollectionData
 *   } CollectionData */
/** @typedef {import('~/types/collection.js').Schemas} Schemas */

function getLastId(data, pk='id') {
  if (data.elems_ids){
    return { method: 'patch', last_id: `${data.elems_ids[0]}/massive_patch/` }
  }
  const id = data[pk]
  const is_edit = id && !data.is_new
  const method = is_edit ? 'put' : 'post'
  const last_id = is_edit ? `${id}/` : ''
  return { method, last_id }
}

export const useMainStore = defineStore('main', {
  state: () => ({
    cats: null,
    all_nodes: {},
    schemas: /** @type {Schemas|Object} */ ({}),
    cats_ready: false,
    status: {},
    current_filter_group: null,
    current_filter_group_data: null,
    current_collection: null,
    current_collection_data: /** @type {?CollectionData} */ (null),
  }),
  actions: {
    setFilterGroup(group) {
      this.current_filter_group = group
      if (this.cats_ready)
        this.setFilterGroupData()
    },
    setFilterGroupData() {
      this.current_filter_group_data = this.all_nodes[
        this.current_filter_group]
    },
    setCollection(group) {
      // console.log("setCollection to", group)
      this.current_collection = group
      // console.log("cats_ready", this.cats_ready)
      if (this.cats_ready)
        this.setCollectionData()
    },
    setCollectionData() {
      this.current_collection_data = this.schemas.collections_dict[
        this.current_collection]
    },
    fetchCatalogs() {
      const { $api } = useNuxtApp()
      return new Promise((resolve) => {
        $api.get('/catalogs/all/')
          .then(({data}) => {
            // console.log("fetchCatalogs data", data)
            this.cats = data
            this.schemas = calculateSchemas(data)
            // console.log("schemas", this.schemas)
            this.all_nodes = calculateNewCats(data, this.schemas)
            this.status = calculate_status(data.status_control)
            this.setCollectionData()
            this.setFilterGroupData()
            this.cats_ready = true
            resolve(data)
          })
          .catch(error => {
            devWarn(error)
          })
      })
    },
    async getSimple([group, id], error_msg = null) {
      const { $api } = useNuxtApp()
      try {
        let response = await $api.get(`/${group}/${id}/`);
        return ok(response)
      } catch (error) {
        return fail(error, error_msg)
      }
    },
    async saveSimple([collection, data], error_msg = null) {
      const { $api } = useNuxtApp()
      const pk = this.schemas.collections_dict[collection]?.pk || 'id'
      const { method, last_id } = getLastId(data, pk)
      try {
        let response = await $api[method](
          `/${collection}/${last_id}`, data, { timeout: 300000 }
        );
        return ok(response)
      } catch (error) {
        return fail(error, error_msg)
      }
    },
    async saveAction([collection, id, action_name], error_msg = null) {
      const { $api } = useNuxtApp()
      try {
        let response = await $api.post(
          `/${collection}/${id}/${action_name}/`
        );
        return ok(response)
      } catch (error) {
        return fail(error, error_msg)
      }
    },
    /** @param {[CollectionData, Object]} args */
    async saveCatalog([collection_data, data], error_msg = null) {
      const { $api } = useNuxtApp()
      const { pk } = collection_data
      const { method, last_id } = getLastId(data, pk)
      const collection = collection_data.snake_name
      const full_url = `catalogs/${collection}/${last_id}`
      try {
        let response = await $api[method](full_url, data);
        if (method === 'post')
          this.cats[collection].unshift(response.data)
        else {
          const index = this.cats[collection].findIndex(
            el => el[pk] === response.data[pk])
          this.cats[collection][index] = response.data
        }
        this.all_nodes = calculateNewCats(this.cats, this.schemas)
        return ok(response)
      } catch (error) {
        return fail(error, error_msg)
      }
    },
    async patchSimple([collection, id, data], error_msg = null) {
      const { $api } = useNuxtApp()
      try {
        let response = await $api.patch(`/${collection}/${id}/`, data);
        return ok(response)
      } catch (error) {
        return fail(error, error_msg)
      }
    },
    /** @param {[CollectionData, number|string, Object]} args */
    async patchCatalog([collection_data, id, data], error_msg = null) {
      const { $api } = useNuxtApp()
      const collection = collection_data.snake_name
      const pk = collection_data.pk || 'id'
      const full_url = `catalogs/${collection}/${id}/`
      try {
        let response = await $api.patch(`${full_url}`, data);
        const index = this.cats[collection].findIndex(
          el => el[pk] === response.data[pk])
        if (index !== -1)
          Object.keys(data).forEach(key => {
            this.cats[collection][index][key] = response.data[key]
          })
        const filter_group = collection_data.filter_group
        if (filter_group){
          this.all_nodes[filter_group.key_name] = hydrateFilterGroup(
            filter_group, this.cats, this.schemas.collections_dict)
        }
        // this.cats[collection][index] = response.data
        return ok(response)
      } catch (error) {
        return fail(error, error_msg)
      }
    },
    async deleteSimple([group, id], error_msg = null) {
      const { $api } = useNuxtApp()
      try {
        await $api.delete(`/${group}/${id}/`);
        return { data: true }
      } catch (error) {
        return fail(error, error_msg)
      }
    },
    /** @param {[CollectionData, number|string]} args */
    async deleteCatalog([collection_data, id], error_msg = null) {
      const { $api } = useNuxtApp()
      const collection = collection_data.snake_name
      const full_url = `catalogs/${collection}/${id}/`
      try {
        await $api.delete(full_url);
        this.cleanDelete(collection, id)
        return { data: true }
      } catch (error) {
        return fail(error, error_msg)
      }
    },
    cleanDelete(collection, id) {
      const index = this.cats[collection].findIndex(
        el => el.id === id)
      this.cats[collection].splice(index, 1)
      this.all_nodes = calculateNewCats(this.cats, this.schemas)
    },
    async fetchElements([group, params]) {
      const { $api } = useNuxtApp()
      return new Promise(resolve => {
        // this.setHeader()
        $api.get(`/${group}/`, {
          cancelToken: request.token, params: params })
          .then(({ data }) => {
            return resolve(data)
          })
          .catch(thrown => {
            if (axios.isCancel(thrown)) {
              request = null
              request = axios.CancelToken.source()
              return resolve({ cancelled: true })
            } else {
              devWarn(thrown)
              return resolve({ errors: thrown.response.data })
            }
          })
      })
    },
    cancelFetch() {
      if (request)
        request.cancel("Operation canceled by the user.")
    },
    // async fetchElements([group, params]) {
    //   try {
    //     const result = await $api.get(`/${group}/`,
    //       {params: params, cancelToken: request.token})
    //     return result.data
    //   } catch ((thrown) => {
    //     if (axios.isCancel(thrown))
    //       console.log('Request canceled', thrown.message)
    //     else
    //       console.error(thrown)
    //   })
    // },
    async exportData([group, params]) {
      const { $api } = useNuxtApp()
      return new Promise((resolve, reject) => {
        // this.setHeader()
        $api.get(`/${group}/export_xls/`, {
          params: params,
          responseType: 'blob',
          cancelToken: request.token
        })
          .then(response => {
            const blob = new Blob([response.data],
              {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'})
            const url = window.URL.createObjectURL(blob)
            const link = document.createElement('a')
            link.href = url
            link.setAttribute('download', `export_${group}.xlsx`)
            document.body.appendChild(link)
            link.click()
            resolve({success: true})
          })
          .catch(thrown => {
            if (axios.isCancel(thrown)) {
              request = null
              request = axios.CancelToken.source()
              return resolve({cancelled: true})
            } else {
              devWarn(thrown)
              reject(thrown)
            }
          })
      })
    },
    async saveCollection(data, error_msg = null) {
      const { $api } = useNuxtApp()
      try {
        let response = await $api.put(`collection/${data.snake_name}/`, data);
        return ok(response)
      } catch (error) {
        return fail(error, error_msg)
      }
    },
  },
  getters: {
    status_dict(state) {
      if (!state.cats?.status_control)
        return {}
      let status_dict = {}
      Object.keys(state.status).forEach(group_key=>{
        status_dict[group_key] = {}
        state.status[group_key].forEach(st=>{
          status_dict[group_key][st.name] = st
        })
      })
      return status_dict
    },
    status_filters(state) {
      return state.schemas?.status_filters || {}
    },
    collections_summary(state) {
      return state.schemas.collections.reduce((obj, coll) => {
        obj[coll.snake_name] = {
          'value': coll.snake_name,
          'title': coll.name,
          'name': coll.name,
          'plural_name': coll.plural_name,
          'icon': coll.icon,
          'color': coll.color,
        }
        return obj
      })
    },
    all_users(state) {
      if (!state.cats)
        return []
      return state.cats.user
    },
    // Catálogo de personas usuarias indexado por id
    users_by_id(state) {
      const map = {}
      for (const u of state.cats?.user || [])
        map[u.id] = u
      return map
    },
    full_editors(state) {
      if (!state.cats)
        return []
      return state.cats.user.filter(user => user.full_editor || user.is_superuser)
    },

  },
})