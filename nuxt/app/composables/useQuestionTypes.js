import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useMainStore } from "~/store/index.js";

// Dos llaves de uso: `name` es la PK que consulta el código y
// `model_question` el puente con la colección del dashboard. Los tipos
// sin modelo de captura (`population`) no entran en el segundo índice.
export function useQuestionTypes() {
  const { cats } = storeToRefs(useMainStore())

  const indexes = computed(() => {
    const by_name = {}
    const by_model = {}
    for (const type of cats.value?.question_type || []) {
      by_name[type.name] = type
      if (type.model_question)
        by_model[type.model_question] = type
    }
    return {by_name, by_model}
  })

  return {
    types_by_name: computed(() => indexes.value.by_name),
    types_by_model: computed(() => indexes.value.by_model),
  }
}
