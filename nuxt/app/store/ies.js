export const useIesStore = defineStore('ies', {
  state: () => ({
    ies_data: null,
    current_period: null,
    surveys: [],
    // packages: [],
  }),
  actions: {
    setIesData(main_ies, ies_details) {
      // console.log("setIesData", main_ies, ies_details)
      this.ies_data = main_ies;
      this.surveys = ies_details.surveys || []
      // this.packages = ies_details.packages || []
      // const last_survey = data?.surveys?.length
      //   ? data.surveys[data.surveys.length - 1]
      //   : {};
      // this.current_period = last_survey.period
      // this.setCurrentPeriod(last_survey.period || null);
    },
    purgeIesData() {
      this.ies_data = null;
      this.surveys = []
      // this.packages = []
      this.current_period = null
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
      // console.log("state", state)
      if (!state.surveys) return [];
      const yearsSet = new Set();
      state.surveys.forEach(survey => {
        yearsSet.add(survey.period)
      });
      const years_list = Array.from(yearsSet).sort((a, b) => b - a);
      return years_list.reduce((list, year) => {
        let year_data = {year}
        year_data.survey = state.surveys.find(s => s.period === year)
        // year_data.package = state.packages.find(p => p.period === year)
        list.push(year_data)
        return list
      }, []);
    },
    all_packages(state) {
      // console.log("state", state)
      if (!state.surveys) return [];
      return state.surveys.reduce((list, survey) => {
        survey.packages.forEach(p => {
          let package_data = { ...p, survey_full: survey, period: survey.period }
          list.push(package_data)
        })
        return list
      }, []);
    },
  },
});