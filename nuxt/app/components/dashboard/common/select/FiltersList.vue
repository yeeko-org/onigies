<script setup>
import SelectGroup from "~/components/dashboard/common/select/SelectGroup.vue";
import TripleBooleanFilter from "~/components/dashboard/custom_filters/TripleBooleanFilter.vue";
import RangeDates from "~/components/dashboard/custom_filters/RangeDates.vue";
import UserSelect from "~/components/dashboard/custom_filters/UserSelect.vue";
import OnlyByFilter from "~/components/dashboard/custom_filters/OnlyByFilter.vue";

const props = defineProps({
  // final_filters: Object,
  visible_filters: Array,
  filter_group: Object,
})
const final_filters = defineModel({type: Object, required: true})
// El padre sigue escuchando @apply-filters; declararlo evita que caiga
// como atributo sobre un template con varias raíces.
defineEmits(['apply-filters'])

</script>
<template>
<!--  <v-col-->
<!--    v-for="filter_box in visible_filters"-->
<!--    :key="filter_box.name"-->
<!--    :order="filter_box.order"-->
<!--    cols="auto"-->
<!--    class="pr-3 pl-0 py-0 d-flex"-->
<!--  >-->
  <template
    v-for="filter_box in visible_filters"
    :key="filter_box.name"
  >
    <div
      v-if="filter_box.key_name"
      class="pr-3 pl-0 py-1 d-flex"
    >
      <SelectGroup
        v-model="final_filters"
        :filter_group_name="filter_box.key_name"
        :category_group_value="filter_box.category_group_value"
        :forced_level="filter_box.forced_level"
        is_filter
      />
    </div>
    <template
      v-else-if="filter_box.component"
    >
      <TripleBooleanFilter
        v-if="filter_box.component === 'TripleBooleanFilter'"
        :final_filters="final_filters"
        :field="filter_box.field"
        :label="filter_box.title"
        class="pr-3 pl-0 py-1"
      />
      <RangeDates
        v-else-if="filter_box.component === 'RangeDates'"
        :final_filters="final_filters"
        :field="filter_box.field"
        :label="filter_box.title"
      />
      <UserSelect
        v-else-if="filter_box.component === 'UserSelect'"
        :final_filters="final_filters"
        :field="filter_box.field"
        :label="filter_box.title"
        class="pr-3 pl-0 py-1"
        is_filter
      />
      <OnlyByFilter
        v-else-if="filter_box.component === 'OnlyByFilter'"
        :final_filters="final_filters"
        :field="filter_box.field"
        :label="filter_box.title"
        :filter_box="filter_box"
        class="pr-3 pl-0 py-1"
      />
      <h5 v-else>{{filter_box.title || filter_box.name}}</h5>
    </template>
    <h5 v-else>{{filter_box.title || filter_box.name}}</h5>
  </template>

</template>