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
            // primary: colors.indigo.darken1,
            // secondary: '#424242',
            // accent: colors.teal.accent4,
            primary: "#8a221f",
            secondary: colors.purple.darken1,
            accent: "#f59322",
          }
        }
      }
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