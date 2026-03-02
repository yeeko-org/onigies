<script setup>
import {computed, onMounted, ref, watch} from 'vue'

const menu_drawer = ref(false)
import {useMainStore} from "~/store/index.js";
import {useAuthStore} from "~/store/auth.js";
import {useIesStore} from "~/store/ies.js";
import {storeToRefs} from "pinia";
const router = useRouter()
const route = useRoute()
const config = useRuntimeConfig();

const mainStore = useMainStore()
const authStore = useAuthStore()
const iesStore = useIesStore()
// const { cats } = storeToRefs(mainStore)
const { setCurrentPeriod } = iesStore;
const { ies_data, current_period } = storeToRefs(iesStore);
// const { fetchCatalogs } = mainStore
const { logout } = authStore
const admin_url = config.public.adminUrl
// console.log('ADMIN URL:', config.public.adminUrl, admin_url)
// const route = useRoute()

// onBeforeMount(() => {
//   console.log("cats_ready")
// //   fetchCatalogs().then(() => {
// //     console.log("cats_ready")
// //   })
// })

const main_items = [
  {
    plural_name: 'Inicio',
    snake_name: '',
    icon: 'home',
    color: 'teal',
  },
  {
    plural_name: 'Personas usuarias',
    snake_name: 'surveys',
    icon: 'account_box',
    color: 'deep-purple',
    disabled: true,
  },
]

const disable_open = ref(false)
const group = ref(null)

function openIcon(val){
  // console.log('openIcon', val)
  disable_open.value = true
}

function openItem(ev, val){
  // console.log('openItem', val)
  // console.log('ev', ev)
  // console.log('disable_open', disable_open.value)
  if (!disable_open.value)
    router.push(`/dashboard/${val}`)
  disable_open.value = false
  // :to="`/dashboard/${collection.snake_name}`"
  // router.push(val)
}

watch(
  group, (val) => {
    // console.log('group', val)
    menu_drawer.value = false
  }
)

const current_year = computed({
  get(){
    return current_period.value
  },
  set(val){
    setCurrentPeriod(val)
  }
})

onMounted(() => {
  console.log("router", router)
  console.log("route", route)
})

const current_page = computed(() => {
  // const fullPath = `respuestas/${route.fullPath}`
  const item = main_items.find(i =>
    route.fullPath === `/respuestas/${i.snake_name}`
  )
  console.log("current_page", item)
  return item || {plural_name: 'Respuestas', icon: 'ballot'}
})

</script>

<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
      flat
      class="mt-n1"
      clipped-left
      height="48"
    >
      <v-app-bar-nav-icon
        @click.stop="menu_drawer = !menu_drawer"
        color="white"
        class="mt-1"
      ></v-app-bar-nav-icon>
      <client-only>
        <v-toolbar-title class="d-flex align-center mt-1">
          <v-icon class="mr-3" color="white">
            {{ current_page?.icon || 'ballot' }}
          </v-icon>
          <span>
            {{current_page.plural_name || 'Respuestas'}}
            {{ies_data && ies_data.acronym}}

          </span>
        </v-toolbar-title>
        <v-select
          v-model="current_year"
          :items="iesStore.available_years"
          label="Año"
          class="mx-4"
          variant="filled"
          density="compact"
          item-title="year"
          item-value="year"
          style="max-width: 100px;"
          xbg-color="white"
          hide-details
        ></v-select>
      </client-only>
      <v-spacer></v-spacer>
      <v-btn
        @click="logout"
        color="white"
        light
        outlined
        icon="logout"
        v-tooltip:bottom="'Cerrar sesión'"
      >
      </v-btn>
    </v-app-bar>
    <v-navigation-drawer
      v-model="menu_drawer"
      app

      mobile-breakpoint="960"
      width="280"
    >
      <v-list nav open-strategy="multiple" _active-class="text-primary">
        <v-list-item>
          <template v-slot:prepend v-if="false">
            <v-icon>dashboard</v-icon>
          </template>
          <v-list-item-title class="text-h6">
            ONIGIES
          </v-list-item-title>
          <v-list-item-subtitle>
            Registro de Respuestas
          </v-list-item-subtitle>
        </v-list-item>
        <v-divider></v-divider>
        <client-only>
          <template
            v-for="collection in main_items"
            :key="collection.plural_name"
          >
            <v-list-item
              :value="collection.snake_name"
              exact
              _active-class="text-accent"
              :disabled="collection.disabled"
              :to="`/respuestas/${collection.snake_name}`"
              :prepend-icon="collection.icon"
              :base-color="collection.color || 'grey-darken-1'"
              :title="collection.plural_name"
            ></v-list-item>
            <v-divider></v-divider>
          </template>
          <template
            v-for="period in iesStore.available_years"
            :key="period.year"
          >
            <v-list-item
              :value="period.year"
              exact
              :to="`/respuestas/${period.year}`"
              base-color="primary"
              :title="`Respuestas ${period.year}`"
            ></v-list-item>
            <v-divider></v-divider>
          </template>

        </client-only>
        <v-divider></v-divider>

      </v-list>
    </v-navigation-drawer>
    <v-main>
      <v-container
        _style="width: 100%;"
        class="pt-0"
        fluid
      >
        <v-layout align-center justify-center >
          <client-only>
            <NuxtPage/>
          </client-only>
        </v-layout>
      </v-container>
    </v-main>
  </v-app>
</template>
