// import ApiService from "./common";
// import { mande } from 'mande'
import { defineStore } from 'pinia'
import axios from "axios";
import { calculateNewCats, hydrateFilterGroup } from "~/composables/nodes.js";
import { calculateSchemas } from "~/composables/cats.js";
import { calculate_status } from "~/composables/filters.js";
let request = axios.CancelToken.source();

function getLastId(data) {
  if (data.elems_ids){
    return { method: 'patch', last_id: `${data.elems_ids[0]}/massive_patch/` }
  }
    // return { method: 'post', last_id: 'massive_edit/' }
  const id = data.id || data.key_name
  // const id = data.id
  const is_edit = data.id && !data.is_new
  const method = is_edit ? 'put' : 'post'
  const last_id = is_edit ? `${id}/` : ''
  return { method, last_id }
}

export const useMainStore = defineStore('main', {
  state: () => ({
    cats: null,
    all_nodes: {},
    schemas: {},
    cats_ready: false,
    status: {},
    current_filter_group: null,
    current_filter_group_data: null,
    current_collection: null,
    current_collection_data: null,
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
            console.log("previous to setCollectionData")
            this.setCollectionData()
            this.setFilterGroupData()
            this.cats_ready = true
            resolve(data)
          })
          .catch(error => {
            console.error(error)
          })
      })
    },
    async getSimple([group, id]) {
      // this.setHeader()
      const { $api } = useNuxtApp()
      try {
        let response = await $api.get(`/${group}/${id}/`);
        return response.data
      } catch (error) {
        console.error(error)
        ;
      }
    },
    async saveSimple([collection, data]) {
      // this.setHeader()
      const { $api } = useNuxtApp()
      const { method, last_id } = getLastId(data)
      try {
        let response = await $api[method](
          `/${collection}/${last_id}`, data,
          { timeout: 300000 }
        );
        return response.data
      } catch (error) {
        console.error(error);
        return {errors: error.response.data}
      }
    },
    async saveAction([collection, id, action_name]) {
      // this.setHeader()
      const { $api } = useNuxtApp()
      try {
        let response = await $api.post(
          `/${collection}/${id}/${action_name}/`
        );
        return response.data
      } catch (error) {
        console.error(error);
        return {errors: error.response.data}
      }
    },
    async saveCatalog([collection_data, data]) {
      // this.setHeader()
      const { $api } = useNuxtApp()
      const { method, last_id } = getLastId(data)
      const collection = collection_data.snake_name
      const full_url = `catalogs/${collection}/${last_id}`
      try {
        let response = await $api[method](full_url, data);
        if (method === 'post')
          this.cats[collection].unshift(response.data)
        else {
          const elem_id = response.data.id ? 'id' : 'key_name'
          const index = this.cats[collection].findIndex(
            el => el[elem_id] === response.data[elem_id])
          this.cats[collection][index] = response.data
        }
        this.all_nodes = calculateNewCats(this.cats, this.schemas)
        return response.data
      } catch (error) {
        console.error(error);
        return {errors: error.response.data}
      }
    },
    async patchSimple([collection, id, data]) {
      // this.setHeader()
      const { $api } = useNuxtApp()
      try {
        let response = await $api.patch(`/${collection}/${id}/`, data);
        return response.data
      } catch (error) {
        console.error(error);
      }
    },
    async patchCatalog([collection_data, id, data]) {
      // this.setHeader()
      const { $api } = useNuxtApp()
      const collection = collection_data.snake_name
      const full_url = `catalogs/${collection}/${id}/`
      try {
        let response = await $api.patch(`${full_url}`, data);
        const index = this.cats[collection].findIndex(
          el => el.id === response.data.id)
        Object.keys(data).forEach(key => {
          this.cats[collection][index][key] = response.data[key]
        })
        const filter_group = collection_data.filter_group
        if (filter_group){
          this.all_nodes[filter_group.key_name] = hydrateFilterGroup(
            filter_group, this.cats, this.schemas.collections_dict)
        }
        // this.cats[collection][index] = response.data
        return response.data
      } catch (error) {
        console.error(error);
      }
    },
    async deleteSimple([group, id]) {
      // this.setHeader()
      const { $api } = useNuxtApp()
      try {
        await $api.delete(`/${group}/${id}/`);
        return {success: true}
      } catch (error) {
        console.error(error);
        return {errors: error.response.data}
      }
    },
    async deleteCatalog([collection_data, id]) {
      // this.setHeader()
      const { $api } = useNuxtApp()
      const collection = collection_data.snake_name
      const full_url = `catalogs/${collection}/${id}/`
      try {
        await $api.delete(full_url);
        this.cleanDelete(collection, id)
        // return id
        return {success: true}
      } catch (error) {
        console.error(error);
        return {errors: error.response.data}
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
              console.error(thrown)
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
              console.error(thrown)
              reject(thrown)
            }
          })
      })
    },
    async saveFile([elem_id, file_data, coll_name]) {
      const { $api } = useNuxtApp()
      try {
        // console.log('elem_id', elem_id)
        let response = await $api.post(
          `/${coll_name}/${elem_id}/add_file/`, file_data,
          {headers: {'Content-Type': 'multipart/form-data'
          }});
        return response.data
      } catch (error) {
        console.error(error);
      }
    },
    async saveCollection(data) {
      const { $api } = useNuxtApp()
      // this.setHeader()
      try {
        let response = await $api.put(`collection/${data.snake_name}/`, data);
        return response.data
      } catch (error) {
        console.error(error);
        return {errors: error.response.data}
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
    full_editors(state) {
      if (!state.cats)
        return []
      return state.cats.user.filter(user => user.full_editor || user.is_superuser)
    },

  },
})