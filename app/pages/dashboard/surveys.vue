<script setup>

import {useMainStore} from "~/stores/index.js";
import GoodPracticeListOld from "~/components/dashboard/example/GoodPracticeListOld.vue";
import GoodPracticeList from "~/components/dashboard/example/goodpractice/GoodPracticeList.vue";
// import {storeToRefs} from 'pinia'
const mainStore = useMainStore()
// const { cats } = storeToRefs(mainStore)

definePageMeta({
  middleware: 'dashboard',
  layout: 'dashboard',
})

const tab = ref(null)

const all_axis = computed(() => mainStore.cats?.axis || [])

</script>

<template>
  <v-card style="width: 100%">
    <v-card-title>
      Ejemplo: 2026
    </v-card-title>

    <v-tabs
      v-model="tab"
      align-tabs="center"
      color="deep-purple-accent-4"
    >
      <v-tab :value="0">Datos iniciales</v-tab>
<!--      <v-tab :value="1">City</v-tab>-->
      <v-tab
        v-for="axis in all_axis"
        :key="axis.id"
        :value="axis.id"
        :color="axis.color"
        :base-color="axis.color"
      >
        <v-icon left :color="axis.color">
          {{ axis.icon }}
        </v-icon>
        {{ axis.short_name }}
      </v-tab>
      <v-tab
        :value="8"
        color="pink"
        base-color="pink"
      >
        <v-icon left color="pink">
          lightbulb
        </v-icon>
        Buenas prácticas
      </v-tab>
    </v-tabs>

    <v-tabs-window v-model="tab">
      <v-tabs-window-item
        v-for="n in 6"
        :key="n-1"
        :value="n-1"
      >
        <v-container fluid>
          <v-row>
            <v-col
              v-for="i in 6"
              :key="i"
              cols="12"
              md="4"
            >
              <v-img
                :lazy-src="`https://picsum.photos/10/6?image=${i * n * 5 + 10}`"
                :src="`https://picsum.photos/500/300?image=${i * n * 5 + 10}`"
                height="205"
                cover
              ></v-img>
            </v-col>
          </v-row>
        </v-container>
      </v-tabs-window-item>
      <v-tabs-window-item
        :value="8"
      >
        <v-container fluid>
          <GoodPracticeList
            :good-practice-package="{id: 5}"
          />
        </v-container>

      </v-tabs-window-item>

    </v-tabs-window>
  </v-card>
</template>

<style scoped>

</style>