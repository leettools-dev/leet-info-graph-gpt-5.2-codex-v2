<template>
  <div class="space-y-3">
    <MessageBubble
      v-for="message in messages"
      :key="message.message_id"
      :message="message"
      :role-label="resolveRoleLabel(message.role)"
    />
  </div>
</template>

<script setup>
import MessageBubble from './MessageBubble.vue'

const props = defineProps({
  messages: {
    type: Array,
    default: () => [],
  },
  roleLabel: {
    type: Function,
    default: null,
  },
})

const resolveRoleLabel = (role) => (props.roleLabel ? props.roleLabel(role) : role)
</script>
