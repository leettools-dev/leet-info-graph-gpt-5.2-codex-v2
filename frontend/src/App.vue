<template>
  <div class="min-h-screen bg-gray-50 text-gray-900">
    <header class="border-b bg-white">
      <div class="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-4 px-6 py-4">
        <div class="font-semibold">{{ t('common.appName') }}</div>
        <div class="flex flex-wrap items-center gap-4 text-sm text-gray-500">
          <div>
            {{ t('common.backendLabel') }}
            <span :class="healthClass">{{ healthLabel }}</span>
          </div>
          <div v-if="authStore.user" class="text-gray-700">
            {{ t('common.userLabel') }} {{ authStore.user.name }} ({{ authStore.user.email }})
          </div>
          <el-button
            v-if="authStore.isAuthenticated"
            size="small"
            :aria-label="t('common.logout')"
            @click="handleLogout"
          >
            {{ t('common.logout') }}
          </el-button>
        </div>
      </div>
      <nav class="mx-auto max-w-5xl px-6 pb-4">
        <RouterLink class="mr-4 text-sm font-medium text-blue-600" to="/login">
          {{ t('common.navLogin') }}
        </RouterLink>
        <RouterLink class="mr-4 text-sm font-medium text-blue-600" to="/chat">
          {{ t('common.navChat') }}
        </RouterLink>
        <RouterLink class="text-sm font-medium text-blue-600" to="/history">
          {{ t('common.navHistory') }}
        </RouterLink>
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
import { useI18n } from 'vue-i18n'
import { useAppStore } from './stores/modules/app'
import { useAuthStore } from './stores/modules/auth'

const appStore = useAppStore()
const authStore = useAuthStore()
const { t } = useI18n()

const healthLabel = computed(() =>
  appStore.backendHealthy ? t('common.backendConnected') : t('common.backendUnavailable')
)
const healthClass = computed(() =>
  appStore.backendHealthy ? 'text-green-600' : 'text-red-600'
)

const handleLogout = async () => {
  await authStore.logout()
}

onMounted(() => {
  appStore.checkBackend()
  authStore.hydrate()
})
</script>
