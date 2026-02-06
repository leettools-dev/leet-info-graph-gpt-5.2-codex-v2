<template>
  <section class="space-y-4 rounded-lg border bg-white p-6 shadow-sm">
    <header class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-xl font-semibold">Chat</h1>
        <p class="mt-2 text-sm text-gray-500">Start a new research session.</p>
      </div>
      <button
        class="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-700"
        type="button"
        @click="isDialogOpen = true"
      >
        New Research
      </button>
    </header>

    <div class="rounded-md border border-dashed border-slate-200 p-6 text-sm text-slate-500">
      Chat interface placeholder.
    </div>

    <div v-if="errorMessage" class="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-600">
      {{ errorMessage }}
    </div>
  </section>

  <el-dialog v-model="isDialogOpen" title="Start new research" width="480px">
    <div class="space-y-3">
      <label class="text-sm font-medium text-slate-700" for="prompt">Prompt</label>
      <el-input
        id="prompt"
        v-model="prompt"
        :rows="4"
        type="textarea"
        placeholder="Describe the research topic you want to explore"
      />
    </div>
    <template #footer>
      <div class="flex justify-end gap-2">
        <el-button @click="handleCancel">Cancel</el-button>
        <el-button :loading="isSubmitting" type="primary" @click="handleCreate">
          Create session
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { useSessionStore } from '../../stores/modules/session'

const router = useRouter()
const sessionStore = useSessionStore()

const isDialogOpen = ref(false)
const prompt = ref('')
const isSubmitting = ref(false)
const errorMessage = ref('')

const handleCancel = () => {
  isDialogOpen.value = false
  prompt.value = ''
  errorMessage.value = ''
}

const handleCreate = async () => {
  if (!prompt.value.trim()) {
    errorMessage.value = 'Please enter a research prompt.'
    return
  }
  isSubmitting.value = true
  errorMessage.value = ''
  try {
    const session = await sessionStore.createSession(prompt.value.trim())
    isDialogOpen.value = false
    prompt.value = ''
    await router.push({ name: 'session-detail', params: { sessionId: session.session_id } })
  } catch (error) {
    errorMessage.value = 'Unable to create a session. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}
</script>
