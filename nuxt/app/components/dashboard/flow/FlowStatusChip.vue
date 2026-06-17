<script setup>
defineProps({
  status: { type: Object, default: null },
  size: { type: String, default: 'default' },
})
</script>

<template>
  <v-chip
    v-if="status"
    :color="status.color || 'grey'"
    :size="size"
    variant="tonal"
  >
    <v-icon start :color="status.color || 'grey'">
      {{ status.icon || 'trip_origin' }}
    </v-icon>
    {{ status.public_name }}
  </v-chip>
</template>
