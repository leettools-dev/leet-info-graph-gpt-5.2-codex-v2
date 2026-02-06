<template>
  <article :class="wrapperClass">
    <div class="max-w-[70%]">
      <p class="text-[10px] uppercase tracking-wide text-slate-400">
        {{ roleLabelText }}
      </p>
      <p class="mt-1 rounded-md px-3 py-2 text-sm" :class="bubbleClass">
        {{ message.content }}
      </p>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  message: {
    type: Object,
    required: true,
  },
  roleLabel: {
    type: String,
    default: '',
  },
})

const wrapperClass = computed(() =>
  props.message.role === 'user' ? 'flex justify-end' : 'flex justify-start'
)

const bubbleClass = computed(() => {
  if (props.message.role === 'user') {
    return 'bg-blue-50 text-blue-900'
  }
  if (props.message.role === 'assistant') {
    return 'bg-slate-100 text-slate-800'
  }
  return 'bg-amber-50 text-amber-900'
})

const roleLabelText = computed(() => props.roleLabel || props.message.role)
</script>
