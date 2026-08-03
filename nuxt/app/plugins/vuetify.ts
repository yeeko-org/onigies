// import '@mdi/font/css/materialdesignicons.css'
// import 'material-design-icons-iconfont/dist/material-design-icons.css'
import '@fontsource/roboto/300.css'
import '@fontsource/roboto/400.css'
import '@fontsource/roboto/500.css'
import '@fontsource/roboto/700.css'
import { h } from 'vue'
// import { aliases, md } from 'vuetify/iconsets/md'
import { aliases as mdAliases } from 'vuetify/iconsets/md'
import colors from 'vuetify/lib/util/colors'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { VDateInput } from "vuetify/labs/VDateInput"


const materialSymbols = {
  component: (props: { tag: string; icon: string }) =>
    h(props.tag, { class: 'material-symbols-outlined' }, props.icon),
}

export default defineNuxtPlugin((nuxtApp) => {
  const vuetify = createVuetify({
    components: {
      VDateInput
    },
    theme: {
      themes: {
        light: {
          dark: false,
          colors: {
            // ONIGIES design system — ver design-system/
            // primary: índigo profundo (chrome del dashboard, layout
            // institucional). accent: turquesa, color de acción para
            // CTAs y botones — los botones DEBEN usar accent, no primary.
            primary: "#2C2F6E",   // --indigo-700
            secondary: colors.purple.darken1,
            accent: "#14A8A0",    // --turquesa-500
            // Los 4 ejes del índice. Sobrescriben los defaults de
            // Vuetify para que `color="purple|blue|amber|pink"` rinda
            // con la paleta del design system.
            purple: "#6E4BC4",    // Eje · Igualdad de género
            blue:   "#2E8FCC",    // Eje · Inclusión y no discriminación
            amber:  "#F2A53A",    // Eje · Cuidados corresponsables
            pink:   "#E63E9A",    // Eje · Vida libre de violencias
          }
        }
      }
    },
    defaults: {
      VBtn: {
        // Convención ONIGIES: los botones usan el color de acción
        // (turquesa) por default. Si necesitas chrome institucional,
        // pasa color="primary" explícitamente.
        color: 'accent',
      },
    },
    icons: {
      defaultSet: 'ms',
      aliases: mdAliases,
      sets: {
        ms: materialSymbols,
      }
    },
    date: {
      locale: {
        'es-MX': {
          firstDayOfWeek: 0,
          masks: {
              input: 'DD/MM/YYYY',
              date: 'DD/MM/YYYY',
              time: 'HH:mm',
              datetime: 'DD/MM/YYYY HH:mm',
          },
        },
      },
    }
  })
  nuxtApp.vueApp.use(vuetify)
})