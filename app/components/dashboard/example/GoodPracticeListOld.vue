<script setup>

const props = defineProps({
  period_id: {
    type: Number,
    required: true,
  },
})

const good_practices = ref([])

function addGoodPractice() {
  good_practices.value.push({
    title: '',
    description: '',
  })
}

</script>

<template>
  <v-row>
    <v-col cols="12">
      <v-card-title>
        Buenas prácticas
      </v-card-title>

      <v-card-text>
        ¿Durante los últimos tres años, su institución ha implementado alguna política, programa o acción en materia de igualdad de género, no discriminación, cuidados corresponsables y/o una vida libre de violencias que, por su trascendencia o innovación, considere que constituya una práctica exitosa que pudiera ser compartida a nivel nacional?
      </v-card-text>
      <v-card-actions>
        <v-btn
          class="mb-4"
          color="accent"
          variant="outlined"
          prepend-icon="add"
          text="Agregar buena práctica"
          @click="addGoodPractice"
        >
        </v-btn>

      </v-card-actions>
    </v-col>
    <v-col cols="12">
      <v-card-text>
        <v-row
          v-for="(practice, index) in good_practices"
          :key="index"
          class="mb-4"
        >
          {{practice}}
        </v-row>
      </v-card-text>
    </v-col>
  </v-row>


</template>

<style scoped>

</style>