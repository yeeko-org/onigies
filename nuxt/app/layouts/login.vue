<script setup>
import {el} from "vuetify/locale";

const route = useRoute()
console.log("route", route)

const title = computed(() => {
  if (route.name === 'login')
    return 'Inicio de sesión'
  else if (route.name === 'register')
    return 'Registro de usuario'
  else if (route.name === 'forgot-password')
    return 'Recuperar contraseña'

  return 'Página'
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
      <v-toolbar-title class="d-flex align-center">
        <v-icon class="mr-3" color="white">
          dashboard
        </v-icon>
        <span class="text-white">
          ONIGIES - {{ title }}
        </span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-app-bar>
    <v-main>
      <v-container
        class="pt-0"
        width="640"
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
