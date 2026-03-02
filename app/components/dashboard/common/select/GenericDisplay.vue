<script setup>

const props = defineProps({
  element_value: {
    type: [Array, String, Number],
    required: false,
  },
  level: String,
  item_value: {
    type: String,
    default: 'id',
  },
  item_title: {
    type: String,
    default: 'name',
  },
  items: {
    type: Array,
    required: true,
  },
  is_multiple: Boolean,
  show_name: Boolean,
  hide_border: Boolean,
})

defineOptions({ inheritAttrs: false })

const final_value = computed(() => {
  if (props.is_multiple){
    return props.element_value.map(
        item1 => props.items.find(
            item2 => item2[props.item_value] === item1))
  }
  return props.items.find(
    item => item[props.item_value] === props.element_value)
})

const show_icon = computed(() => {
  return ['group', 'type'].includes(props.level) && final_value.value?.icon
})

const show_chip = computed(() => {
  return final_value.value?.color && (props.show_name || !show_icon.value)
})

</script>

<template>
  <div
    class="mr-0 px-2"
    :class="{'white-border': !hide_border}"
  >
    <template v-if="final_value && is_multiple">
      <template v-if="level === 'group'">
        <v-icon
          v-for="item in final_value"
          class="mr-1"
          :color="item.color || 'primary'"
          v-tooltip="item[item_title]"
        >
          {{ item.icon }}
        </v-icon>
      </template>
      <div v-else>
        <div
          v-for="item in final_value"
          class="mr-1"
        >
          {{ item[item_title] }}
        </div>
      </div>
    </template>

    <template v-else-if="final_value">
      <v-chip
        v-if="show_chip"
        :color="final_value.color"
        :prepend-icon="final_value.icon"
        size="small"
        v-bind="$attrs"
      >
        {{ final_value[item_title] }}
      </v-chip>
      <v-icon
        v-else-if="show_icon"
        class="mr-1"
        :color="final_value.color || 'primary'"
        v-tooltip="final_value[item_title]"
        v-bind="$attrs"
      >
        {{ final_value.icon }}
      </v-icon>
      <span
        v-else
      >
        {{ final_value[item_title] }}
      </span>
    </template>
    <span v-else>
      !?
    </span>
  </div>
</template>

<style scoped>
.white-border {
  border-right: 1px solid #e0e0e0;
  border-bottom: 1px solid #e0e0e0;
}
</style>