<script setup>
import { computed } from 'vue'
import { useMainStore } from '~/store/index.js'

const props = defineProps({
  main: { type: Object, required: true },
  collection: { type: String, required: true },
  fromCode: { type: String, required: true },
  toCode: { type: String, required: true },
  canTransition: { type: Function, default: () => true },
  missingItems: { type: Function, default: () => [] },
  size: { type: String, default: 'small' },
})

const emit = defineEmits(['change', 'blocked'])

const mainStore = useMainStore()

const field = computed(() => {
  if (props.collection.includes('status_'))
    return props.collection
  return `status_${props.collection}`
})

const simpleName = computed(() =>
  props.collection.replace('status_', '')
)

const currentCode = computed(() => props.main[field.value])
const isFrom = computed(() => currentCode.value === props.fromCode)
const isTo = computed(() => currentCode.value === props.toCode)

const fromItem = computed(() =>
  mainStore.status_dict?.[simpleName.value]?.[props.fromCode] || {}
)
const toItem = computed(() =>
  mainStore.status_dict?.[simpleName.value]?.[props.toCode] || {}
)

function onToggle(value) {
  if (!value || value === currentCode.value) return
  if (value === props.toCode && !props.canTransition()) {
    emit('blocked', props.missingItems())
    return
  }
  emit('change', value)
}
</script>

<template>
  <v-btn-toggle
    :model-value="currentCode"
    mandatory
    density="compact"
    @update:model-value="onToggle"
  >
    <v-btn
      :value="fromCode"
      :color="fromItem.color || 'grey'"
      :variant="isFrom ? 'flat' : 'outlined'"
      :size="size"
    >
      <v-icon start :size="size">
        {{ fromItem.icon || 'radio_button_unchecked' }}
      </v-icon>
      {{ fromItem.public_name || fromCode }}
    </v-btn>
    <v-btn
      :value="toCode"
      :color="toItem.color || 'grey'"
      :variant="isTo ? 'flat' : 'outlined'"
      :size="size"
    >
      <v-icon start :size="size">
        {{ toItem.icon || 'radio_button_unchecked' }}
      </v-icon>
      {{ toItem.public_name || toCode }}
    </v-btn>
  </v-btn-toggle>
</template>