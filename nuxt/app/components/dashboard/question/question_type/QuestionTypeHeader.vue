<script setup>
import HeaderCommon from "~/components/dashboard/common/generic/HeaderCommon.vue";
import HeaderChip from "~/components/dashboard/common/utils/HeaderChip.vue";

defineProps({
  main: Object,
  collection_data: Object,
  show_details: {
    type: Boolean,
    default: false,
  },
})

</script>

<template>
  <HeaderCommon
    :main="main"
    :show_details="show_details"
    :collection_data="collection_data"
  >
    <template #details>
      <div class="d-flex align-center ga-2">
        <HeaderChip
          :count="main.observables_count"
          collection_name="observable"
          label="observable"
          label_plural="observables"
          :tooltip_title="main.public_name"
        />
      </div>
    </template>
  </HeaderCommon>
</template>

<style scoped>

</style>
