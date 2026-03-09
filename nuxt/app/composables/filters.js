import colorMixin from "~/mixins/colorMixin.js";

export const status_filters = {
  "status_sending": {
    name: "de Envío",
    short_name: "Envío",
    hidden: false,
    key_name: "sending",
    collection: "status_sending",
    order: 4,
    default_value: "draft",
  },
  "status_register": {
    name: "de Registro",
    short_name: "Registro",
    hidden: false,
    key_name: "register",
    collection: "status_register",
    order: 4,
    default_value: "pre_start",
  },
  "status_validation": {
    name: "de Validación",
    short_name: "Validación",
    hidden: false,
    key_name: "validation",
    collection: "status_validation",
    order: 5,
    default_value: "proposed",
  },
  // "status_location": {
  //   name: "de Ubicación",
  //   short_name: "Ubicación",
  //   hidden: false,
  //   key_name: "location",
  //   collection: "status_location",
  //   order: 6,
  // },
  // "status_retro": {
  //   name: "de Retroalimentación",
  //   short_name: "Feedback",
  //   hidden: false,
  //   key_name: "retro",
  //   collection: "status_retro",
  //   order: 6,
  // }
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



