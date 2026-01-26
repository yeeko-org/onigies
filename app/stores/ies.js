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
    setCurrentPeriod(period) {
      this.current_period = period;
      if (!period) return;
      const router = useRouter()
      return router.push({ path: `/respuestas/${period}` });
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