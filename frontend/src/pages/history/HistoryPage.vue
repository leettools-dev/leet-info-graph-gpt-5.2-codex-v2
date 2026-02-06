<template>
  <section class="space-y-4 rounded-lg border bg-white p-6 shadow-sm">
    <header class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-xl font-semibold">History</h1>
        <p class="mt-2 text-sm text-gray-500">Your recent research sessions.</p>
      </div>
      <el-button type="primary" @click="goToChat">New Research</el-button>
    </header>

    <div v-if="isLoading" class="text-sm text-slate-500">Loading sessions...</div>
    <div v-else-if="errorMessage" class="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-600">
      {{ errorMessage }}
    </div>
    <div v-else class="space-y-3">
      <article
        v-for="session in sessions"
        :key="session.session_id"
        class="flex flex-wrap items-center justify-between gap-4 rounded-md border border-slate-200 p-4"
      >
        <div>
          <p class="text-sm font-semibold text-slate-900">{{ session.prompt }}</p>
          <p class="mt-1 text-xs text-slate-500">Status: {{ session.status }}</p>
        </div>
        <div class="flex items-center gap-2">
          <el-button type="primary" plain @click="openSession(session.session_id)">
            View
          </el-button>
          <el-button type="danger" plain @click="removeSession(session.session_id)">
            Delete
          </el-button>
        </div>
      </article>
      <p v-if="!sessions.length" class="text-sm text-slate-500">
        No sessions yet. Create a new research session to get started.
      </p>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { useSessionStore } from '../../stores/modules/session'

const router = useRouter()
const sessionStore = useSessionStore()

const sessions = computed(() => sessionStore.sessions)
const isLoading = computed(() => sessionStore.status === 'loading')
const errorMessage = computed(() => (sessionStore.status === 'error' ? 'Unable to load sessions.' : ''))

const loadSessions = async () => {
  try {
    await sessionStore.fetchSessions({ limit: 20, offset: 0 })
  } catch (error) {
    // error handled by store
  }
}

const openSession = (sessionId) => {
  router.push({ name: 'session-detail', params: { sessionId } })
}

const removeSession = async (sessionId) => {
  try {
    await sessionStore.removeSession(sessionId)
  } catch (error) {
    // error handled by store
  }
}

const goToChat = () => {
  router.push({ name: 'chat' })
}

onMounted(loadSessions)
</script>
