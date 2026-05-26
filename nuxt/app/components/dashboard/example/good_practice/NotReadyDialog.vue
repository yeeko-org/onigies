<script setup>

defineProps({
  goodPractices: {
    type: Array,
    required: true,
  },
  notReadyDetails: {
    type: Array,
    required: true,
  },
});
const dialog_visible = defineModel({ type: Boolean, default: false });

</script>

<template>
  <v-dialog
    v-model="dialog_visible"
    max-width="640"
  >
    <v-card>
      <v-card-title class="headline">
        Aún no puedes enviar las buenas prácticas
      </v-card-title>
      <v-card-text>
        <v-alert
          type="info"
          variant="tonal"
          class="mb-3"
        >
          Todas tus buenas prácticas deben estar en el estado
          <b>"Lista para enviar"</b> antes de enviar el paquete
          a revisión.
        </v-alert>
        <div
          v-if="!goodPractices.length"
          class="text-body-2"
        >
          Aún no has agregado ninguna buena práctica.
        </div>
        <div v-else>
          <div class="text-body-2 mb-2">
            Estas prácticas aún no están listas:
          </div>
          <ul class="ml-4">
            <li
              v-for="p in notReadyDetails"
              :key="p.id"
              class="mb-1"
            >
              <b>{{ p.name }}</b>
              <template v-if="p.missing.length">
                — falta: {{ p.missing.join(', ') }}
              </template>
              <template v-else>
                — falta marcarla como "Lista para enviar"
              </template>
            </li>
          </ul>
        </div>
      </v-card-text>
      <v-card-actions class="mx-3 mb-2">
        <v-spacer />
        <v-btn
          variant="elevated"
          color="primary"
          @click="dialog_visible = false"
        >
          Entendido, regresar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>