<template>
  <section class="space-y-4 rounded-lg border bg-white p-6 shadow-sm">
    <header class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-xl font-semibold">Session Details</h1>
        <p v-if="session" class="mt-2 text-sm text-gray-500">
          {{ session.prompt }}
        </p>
      </div>
      <el-button type="primary" @click="goToHistory">Back to History</el-button>
    </header>

    <div v-if="isLoading" class="text-sm text-slate-500">Loading session...</div>
    <div v-else-if="errorMessage" class="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-600">
      {{ errorMessage }}
    </div>
    <div v-else class="space-y-4">
      <SourceList :sources="sources" :loading="sourcesLoading" />
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

import { listSources } from '../../api/source'
import SourceList from '../../components/source/SourceList.vue'
import { useSessionStore } from '../../stores/modules/session'

const route = useRoute()
const router = useRouter()
const sessionStore = useSessionStore()
const { t } = useI18n()

const session = computed(() => sessionStore.activeSession)
const isLoading = computed(() => sessionStore.status === 'loading')
const loadError = computed(() => sessionStore.status === 'error')
const localError = ref('')
const errorMessage = computed(() =>
  localError.value || (loadError.value ? t('common.sessionDetailLoadError') : '')
)

const sources = ref([])
const sourcesLoading = ref(false)

const loadSession = async () => {
  const { sessionId } = route.params
  if (!sessionId) {
    localError.value = t('common.sessionDetailMissingId')
    return
  }
  localError.value = ''
  try {
    await sessionStore.fetchSession(sessionId)
  } catch (error) {
    // error handled by store
  }
}

const loadSources = async () => {
  const { sessionId } = route.params
  if (!sessionId) {
    sources.value = []
    return
  }
  sourcesLoading.value = true
  try {
    const { data } = await listSources(sessionId)
    sources.value = data
  } catch (error) {
    sources.value = []
  } finally {
    sourcesLoading.value = false
  }
}

const goToHistory = () => {
  router.push({ name: 'history' })
}

onMounted(async () => {
  await loadSession()
  await loadSources()
})
</script>
