import colorMixin from "~/mixins/colorMixin.js";
import {useMainStore} from "~/store/index.js";

/**
 * @param {string} status_group Nombre del campo, `status_{group}`.
 * @returns {string}
 */
export function statusGroupLabel(status_group) {
  const mainStore = useMainStore()
  const status_info = mainStore.status_filters[status_group]
  return `Status ${status_info?.name || ''}`.trim()
}

export function calculate_status(status_control) {
  return status_control.reduce((obj, st) => {
    st = colorMixin.methods.getComplementColor(st)
    if (obj[st.group])
      obj[st.group].push(st)
    else
      obj[st.group] = [st]
    return obj
  }, {})
}



