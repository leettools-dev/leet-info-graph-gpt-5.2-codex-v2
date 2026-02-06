<template>
  <div class="min-h-screen bg-gray-50 text-gray-900">
    <header class="border-b bg-white">
      <div class="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <div class="font-semibold">Infograph Assistant</div>
        <div class="text-sm text-gray-500">
          Backend: <span :class="healthClass">{{ healthLabel }}</span>
        </div>
      </div>
      <nav class="mx-auto max-w-5xl px-6 pb-4">
        <RouterLink class="mr-4 text-sm font-medium text-blue-600" to="/login">Login</RouterLink>
        <RouterLink class="mr-4 text-sm font-medium text-blue-600" to="/chat">Chat</RouterLink>
        <RouterLink class="text-sm font-medium text-blue-600" to="/history">History</RouterLink>
      </nav>
    </header>
    <main class="mx-auto max-w-5xl px-6 py-6">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useAppStore } from './stores/modules/app'

const appStore = useAppStore()

const healthLabel = computed(() => (appStore.backendHealthy ? 'Connected' : 'Unavailable'))
const healthClass = computed(() =>
  appStore.backendHealthy ? 'text-green-600' : 'text-red-600'
)

onMounted(() => {
  appStore.checkBackend()
})
</script>
