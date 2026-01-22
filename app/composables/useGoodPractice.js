import { ref } from 'vue'
import { useMainStore } from '~/stores/index.js'

export function useGoodPractice() {
  const mainStore = useMainStore()
  const loading = ref(false)
  const error = ref(null)

  const fetchFeatures = async () => {
    try {
      return await mainStore.fetchData('feature')
    } catch (e) {
      error.value = e
      return []
    }
  }

  const fetchGoodPractices = async (packageId) => {
    loading.value = true
    try {
      return await mainStore.fetchData(
        'goodpractice',
        { package: packageId }
      )
    } finally {
      loading.value = false
    }
  }

  const fetchGoodPractice = async (id) => {
    loading.value = true
    try {
      return await mainStore.fetchItem('goodpractice', id)
    } finally {
      loading.value = false
    }
  }

  const deleteGoodPractice = async (id) => {
    loading.value = true
    try {
      return await mainStore.deleteItem('goodpractice', id)
    } finally {
      loading.value = false
    }
  }

  const saveFeatureGoodPractice = async (data) => {
    try {
      if (data.id) {
        return await mainStore.updateItem(
          'featuregoodpractice', data.id, data
        )
      }
      return await mainStore.createItem('featuregoodpractice', data)
    } catch (e) {
      error.value = e
      throw e
    }
  }

  return {
    loading,
    error,
    fetchFeatures,
    fetchGoodPractices,
    fetchGoodPractice,
    deleteGoodPractice,
    saveFeatureGoodPractice
  }
}