<script setup>
import {computed, onMounted, ref, watch} from 'vue'

const menu_drawer = ref(false)
import {useMainStore} from "~/store/index.js";
import {useAuthStore} from "~/store/auth.js";
import {storeToRefs} from "pinia";
const router = useRouter()
const config = useRuntimeConfig();

const mainStore = useMainStore()
const authStore = useAuthStore()
const { schemas, current_collection_data } = storeToRefs(mainStore)
const { is_full_editor } = storeToRefs(authStore);
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
    plural_name: 'Respuestas (IES/Año)',
    snake_name: 'surveys',
    icon: 'ballot',
    color: 'teal',
  },
  {
    plural_name: 'Instituciones',
    snake_name: 'institution',
    icon: 'apartment',
    color: 'indigo',
  },
  {
    plural_name: 'Años de registro',
    snake_name: 'period',
    icon: 'event',
    color: 'brown',
  },
  {
    plural_name: 'Envíos de Buenas Prácticas',
    snake_name: 'good_practice_package',
    icon: 'batch_prediction',
    color: 'pink',
  },
  {
    plural_name: 'Buenas Prácticas',
    snake_name: 'good_practice',
    icon: 'lightbulb',
    color: 'pink',
  },
  // {
  //   plural_name: 'Ejemplo de registro',
  //   snake_name: 'surveys',
  //   icon: 'ballot',
  //   color: 'deep-purple',
  // },
]

const main_collections = [
  {
    title: 'Gestión Catálogos',
    icon: 'category',
    color: 'purple',
    catalogs: [
      {
        plural_name: 'Aspectos Buenas Prácticas',
        snake_name: 'features',
      },
      {
        plural_name: 'Sectores poblacionales',
        snake_name: 'sectors',
      },
      {
        plural_name: 'Ejes y Componentes',
        snake_name: 'axes',
      },
      {
        plural_name: 'Grupos de preguntas',
        snake_name: 'question_groups',
      },
      {
        plural_name: 'Opciones de respuesta',
        snake_name: 'a_options',
      },
    ],
  },
]

const disable_open = ref(false)
const group = ref(null)

const collection_data = computed(() => {
  // console.log('route', route)
  // const group_name = route.params.group
  const dashboard = {
    title: 'Dashboard',
    name: 'Dashboard',
    plural_name: 'Dashboard',
    icon: 'dashboard',
    key: 'dashboard',
  }
  // return all_groups.value.find(g => g.key === group_name) || dashboard
  return current_collection_data.value || dashboard
})

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
            {{ collection_data.icon || (collection_data.parent
                  ? collection_data.parent.icon
                  : 'dashboard') }}
          </v-icon>
          <span class="text-white">
            {{ collection_data.plural_name }}
          </span>
          <v-btn
            v-if="false"
            icon="category"
            _v-tooltip:bottom="'Categorías de ___'"
          ></v-btn>
        </v-toolbar-title>
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
      temporary
      mobile-breakpoint="960"
      width="280"
    >
      <v-list nav open-strategy="multiple" _active-class="text-primary">
        <v-list-item>
          <template v-slot:prepend v-if="false">
            <v-icon>dashboard</v-icon>
          </template>
          <v-list-item-title class="text-h6">
            Dashboard ONIGIES
          </v-list-item-title>
        </v-list-item>
        <v-divider></v-divider>
        <client-only>
          <template
            v-for="collection in main_items"
            :key="collection.snake_name"
          >

            <v-list-item
              :value="collection.snake_name"
              exact
              _active-class="text-accent"
              :to="`/dashboard/${collection.snake_name}`"
              :prepend-icon="collection.icon"
              :base-color="collection.color || 'grey-darken-1'"
              :disabled="!is_full_editor"
              :title="collection.plural_name"
            ></v-list-item>
            <v-divider></v-divider>
          </template>
          <template
            v-for="collection in main_collections"
            :key="collection.snake_name"
          >
            <v-list-group soubgroup>
              <template v-slot:activator="{ props, isOpen }">
                <v-list-item
                  v-bind="props"
                  exact
                  :title="collection.title"
                  :prepend-icon="collection.icon"
                  :base-color="collection.color || 'grey-darken-1'"
                >
                  <template v-slot:append="{ isActive, select }">
                    <v-icon
                      @click="openIcon"
                    >
                      {{ isActive ? 'expand_less' : 'expand_more' }}
                    </v-icon>
                  </template>
                </v-list-item>
              </template>
              <v-list-item
                v-for="cat in collection.catalogs"
                :key="cat.snake_name"
                exact
                :title="cat.plural_name"
                :value="cat.snake_name"
                :to="`/dashboard/catalog/${cat.snake_name}`"
              ></v-list-item>
            </v-list-group>
          </template>

        </client-only>
        <v-divider></v-divider>

        <v-list-item
          :href="`${admin_url}/profile_auth/user/`"
          target="_blank"
          title="Gestión de usuarios"
        >
          <template v-slot:prepend>
            <v-icon color="accent">manage_accounts</v-icon>
          </template>

        </v-list-item>
        <v-list-item
          :href="`${admin_url}/work_flux/statuscontrol/`"
          target="_blank"
          title="Gestión de status"
        >
          <template v-slot:prepend>
            <v-icon color="accent">hub</v-icon>
          </template>
        </v-list-item>
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
