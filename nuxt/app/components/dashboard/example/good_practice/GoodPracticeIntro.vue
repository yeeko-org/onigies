<script setup>
const criteria = [
  'Ser novedosa y/o creativa',
  'Tener relevancia contextual',
  'Tener continuidad (más de 5 años)',
  'Tener respaldo comunitario',
  'Ser replicada por otras instituciones',
  'Tener una amplia cobertura',
  'Ser evaluada positivamente',
]

defineProps({
  maxWidth: { type: [Number, String], default: 760 }
})
</script>

<template>
  <v-dialog :max-width="maxWidth" scrollable>
    <template #activator="{ props: activatorProps }">
      <slot name="activator" :props="activatorProps" />
    </template>
    <template #default="{ isActive }">
      <v-card>
        <v-toolbar color="secondary" density="compact">
          <v-icon start class="ml-3">lightbulb</v-icon>
          <v-toolbar-title>
            ¿Qué es una buena práctica?
          </v-toolbar-title>
          <v-spacer />
          <v-btn icon @click="isActive.value = false">
            <v-icon>close</v-icon>
          </v-btn>
        </v-toolbar>

        <v-card-text class="pa-5 text-body-1">
          <section class="mb-5">
            <div class="text-h6 text-primary mb-2">
              1. Definición
            </div>
            <p>
              Son experiencias de políticas, programas, proyectos o
              acciones institucionales exitosas con metodologías sólidas
              que han logrado transformaciones significativas en las IES
              para la igualdad de género, o bien, que han logrado
              atender de manera notable alguna problemática vinculada
              con la desigualdad de género.
            </p>
          </section>

          <section class="mb-5">
            <div class="text-h6 text-primary mb-2">
              2. Características
            </div>
            <p class="mb-3">
              Las dos principales características de una buena práctica
              son que existen evidencias de que sus resultados han sido
              transformadores de problemáticas vinculadas con la
              desigualdad de género en las IES y que se han implementado
              mediante metodologías sólidas y fundamentadas en el marco
              de las políticas de igualdad de género.
            </p>
            <p class="mb-2">
              Adicionalmente, las buenas prácticas pueden cumplir alguno
              o varios de los siguientes criterios:
            </p>
            <ul class="pl-6">
              <li
                v-for="(criterion, i) in criteria"
                :key="i"
                class="mb-1"
              >
                {{ criterion }}
              </li>
            </ul>
          </section>

          <section class="mb-5">
            <div class="text-h6 text-primary mb-2">
              3. Forma de declarar
            </div>
            <p>
              La forma de declarar una buena práctica ante el ONIGIES es
              narrativa y descriptiva. Se solicita una breve descripción
              general de la buena práctica acompañada de evidencias
              documentales, fotográficas, etc. Adicionalmente, se
              solicita una justificación para cada criterio de buenas
              prácticas que la IES declara cumplir. Se priorizarán
              evidencias formalizadas institucionalmente.
            </p>
          </section>

          <section class="mb-5">
            <div class="text-h6 text-primary mb-2">
              4. Límite
            </div>
            <p>
              Hasta cinco (5) buenas prácticas por IES.
            </p>
          </section>

          <section class="mb-5">
            <div class="text-h6 text-primary mb-2">
              5. Participación opcional
            </div>
            <p>
              No es obligatorio llenar la sección de buenas prácticas.
              En caso de no llenar esta sección, las IES no tendrán
              ninguna penalización en el puntaje final de la medición.
            </p>
          </section>

          <section>
            <div class="text-h6 text-primary mb-2">
              6. Años de referencia
            </div>
            <p>
              Buenas prácticas que hayan estado vigentes en los últimos
              cinco años (2022-2026).
            </p>
          </section>
        </v-card-text>

        <v-card-actions class="mx-3 mb-2">
          <v-spacer />
          <v-btn
            color="primary"
            variant="elevated"
            @click="isActive.value = false"
          >
            Entendido
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>