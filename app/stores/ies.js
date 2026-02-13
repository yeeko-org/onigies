export const useIesStore = defineStore('counter', {
  state: () => ({
    count: 0,
    ies_data: null,
    current_period: null,
  }),
  actions: {
    setCount(value) {
      this.count = value;
    },
    setIesData(data) {
      this.ies_data = data;
      // const last_survey = data?.surveys?.length
      //   ? data.surveys[data.surveys.length - 1]
      //   : {};
      // this.current_period = last_survey.period
      // this.setCurrentPeriod(last_survey.period || null);
    },
    setLogo(logo_url) {
      if (!this.ies_data)
        return
      this.ies_data.logo = logo_url
    },
    setCurrentPeriod(period) {
      this.current_period = period;
      if (!period) return;
      const router = useRouter()
      return router.push({ path: `/respuestas/${period}` });
    },
    //     UPDATE_LOGO({state, commit}, new_data){
    //   commit("SET_IN_LOADING", true)
    //   return new Promise (resolve => {
    //     DashboardService.updateLogo(new_data).then(({data})=>{
    //       commit("SET_IN_LOADING", false)
    //       //console.log(data)
    //       return resolve(commit('SET_IES', data))
    //     })
    //   })
    // },
    async updateLogo({data, institution_id, snack_text}) {
      // this.in_loading = true
      const { $api } = useNuxtApp()
      let response = await $api.post(
        `institution/${institution_id}/upload_logo/`, data,
        {headers: {'Content-Type': 'multipart/form-data'}}
      )
      if (response.errors) {
        return { errors: response.errors }
      } else {
        this.setLogo(response.data.logo)
        // if (snack_text) {
        //   const mainStore = useMainStore()
        //   mainStore.showSnackbar(snack_text, 'success')
        // }
      }
    }
  },
  getters: {
    available_years(state) {
      if (!state.ies_data || !state.ies_data.surveys) return [];
      const yearsSet = new Set();
      state.ies_data.surveys.forEach(survey => {
        yearsSet.add(survey.period)
      });
      return Array.from(yearsSet).sort((a, b) => b - a);
    }
  },
});