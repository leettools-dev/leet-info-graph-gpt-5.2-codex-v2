<template>
  <div class="space-y-2">
    <el-input
      v-model="localValue"
      :placeholder="placeholder"
      :rows="rows"
      type="textarea"
      :disabled="disabled"
      :aria-label="ariaLabel"
      @keydown.enter.exact.prevent="handleSend"
    />
    <div class="flex items-center justify-between">
      <p v-if="hint" class="text-xs text-slate-400">
        {{ hint }}
      </p>
      <span v-else aria-hidden="true"></span>
      <el-button
        :disabled="disabled || !canSend"
        :loading="loading"
        type="primary"
        @click="handleSend"
      >
        {{ sendLabel }}
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: '',
  },
  hint: {
    type: String,
    default: '',
  },
  sendLabel: {
    type: String,
    default: '',
  },
  ariaLabel: {
    type: String,
    default: '',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  rows: {
    type: Number,
    default: 3,
  },
})

const emit = defineEmits(['update:modelValue', 'send'])

const localValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
})

const canSend = computed(() => Boolean(props.modelValue.trim()))

const handleSend = () => {
  if (props.disabled || props.loading || !canSend.value) {
    return
  }
  emit('send')
}
</script>
