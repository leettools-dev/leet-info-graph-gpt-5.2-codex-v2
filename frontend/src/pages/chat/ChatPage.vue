<template>
  <section class="space-y-4 rounded-lg border bg-white p-6 shadow-sm">
    <header class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-xl font-semibold">{{ t('common.chatTitle') }}</h1>
        <p class="mt-2 text-sm text-gray-500">{{ t('common.chatSubtitle') }}</p>
      </div>
      <div class="flex items-center gap-2">
        <el-button v-if="session" plain type="primary" @click="goToSession">
          {{ t('common.viewSession') }}
        </el-button>
        <button
          class="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-700"
          type="button"
          @click="isDialogOpen = true"
        >
          {{ t('common.newResearch') }}
        </button>
      </div>
    </header>

    <div class="rounded-md border border-dashed border-slate-200 p-4 text-sm text-slate-500">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div>
          <p class="text-xs uppercase tracking-wide text-slate-400">
            {{ t('common.activeSessionLabel') }}
          </p>
          <p class="mt-1 text-sm text-slate-700">
            {{ session ? session.prompt : t('common.noActiveSession') }}
          </p>
        </div>
        <el-tag v-if="session" type="info" size="small">{{ session.status }}</el-tag>
      </div>
    </div>

    <div
      ref="messageContainer"
      class="h-96 overflow-y-auto rounded-md border border-slate-200 bg-white p-4"
    >
      <div v-if="isLoadingMessages" class="text-sm text-slate-500">
        {{ t('common.loadingMessages') }}
      </div>
      <div v-else-if="!session" class="text-sm text-slate-500">
        {{ t('common.chatEmpty') }}
      </div>
      <div v-else-if="!messages.length" class="text-sm text-slate-500">
        {{ t('common.chatNoMessages') }}
      </div>
      <div v-else class="space-y-3">
        <article
          v-for="message in messages"
          :key="message.message_id"
          :class="message.role === 'user' ? 'flex justify-end' : 'flex justify-start'"
        >
          <div class="max-w-[70%]">
            <p class="text-[10px] uppercase tracking-wide text-slate-400">
              {{ roleLabel(message.role) }}
            </p>
            <p
              class="mt-1 rounded-md px-3 py-2 text-sm"
              :class="
                message.role === 'user'
                  ? 'bg-blue-50 text-blue-900'
                  : message.role === 'assistant'
                    ? 'bg-slate-100 text-slate-800'
                    : 'bg-amber-50 text-amber-900'
              "
            >
              {{ message.content }}
            </p>
          </div>
        </article>
      </div>
      <div v-if="isSending" class="mt-3 text-xs text-slate-500">
        {{ t('common.chatSending') }}
      </div>
    </div>

    <ChatInput
      v-model="messageInput"
      :placeholder="t('common.chatInputPlaceholder')"
      :hint="t('common.chatInputHint')"
      :send-label="t('common.sendMessage')"
      :aria-label="t('common.chatInputAria')"
      :disabled="!session"
      :loading="isSending"
      @send="handleSend"
    />

    <div v-if="errorMessage" class="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-600">
      {{ errorMessage }}
    </div>
  </section>

  <el-dialog v-model="isDialogOpen" :title="t('common.startNewResearchTitle')" width="480px">
    <div class="space-y-3">
      <label class="text-sm font-medium text-slate-700" for="prompt">
        {{ t('common.promptLabel') }}
      </label>
      <el-input
        id="prompt"
        v-model="prompt"
        :rows="4"
        type="textarea"
        :placeholder="t('common.promptPlaceholder')"
      />
    </div>
    <template #footer>
      <div class="flex justify-end gap-2">
        <el-button @click="handleCancel">{{ t('common.cancel') }}</el-button>
        <el-button :loading="isSubmitting" type="primary" @click="handleCreate">
          {{ t('common.createSession') }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

import { createMessage, listMessages } from '../../api/session'
import ChatInput from '../../components/chat/ChatInput.vue'
import { useSessionStore } from '../../stores/modules/session'

const router = useRouter()
const sessionStore = useSessionStore()
const { t } = useI18n()

const isDialogOpen = ref(false)
const prompt = ref('')
const isSubmitting = ref(false)
const errorMessage = ref('')

const messages = ref([])
const messageInput = ref('')
const isLoadingMessages = ref(false)
const isSending = ref(false)
const messageContainer = ref(null)

const session = computed(() => sessionStore.activeSession)
const canSend = computed(() => Boolean(session.value) && Boolean(messageInput.value.trim()) && !isSending.value)

const roleLabel = (role) => {
  if (role === 'assistant') {
    return t('common.chatRoleAssistant')
  }
  if (role === 'system') {
    return t('common.chatRoleSystem')
  }
  return t('common.chatRoleUser')
}

const handleCancel = () => {
  isDialogOpen.value = false
  prompt.value = ''
  errorMessage.value = ''
}

const handleCreate = async () => {
  if (!prompt.value.trim()) {
    errorMessage.value = t('common.promptRequired')
    return
  }
  isSubmitting.value = true
  errorMessage.value = ''
  try {
    await sessionStore.createSession(prompt.value.trim())
    isDialogOpen.value = false
    prompt.value = ''
  } catch (error) {
    errorMessage.value = t('common.sessionCreateError')
  } finally {
    isSubmitting.value = false
  }
}

const loadMessages = async () => {
  if (!session.value) {
    return
  }
  isLoadingMessages.value = true
  errorMessage.value = ''
  try {
    const { data } = await listMessages(session.value.session_id)
    messages.value = data
  } catch (error) {
    errorMessage.value = t('common.chatLoadError')
  } finally {
    isLoadingMessages.value = false
  }
}

const scrollToBottom = async () => {
  await nextTick()
  const container = messageContainer.value
  if (container) {
    container.scrollTop = container.scrollHeight
  }
}

const handleSend = async () => {
  if (!session.value) {
    errorMessage.value = t('common.chatNoSessionError')
    return
  }
  if (!messageInput.value.trim()) {
    errorMessage.value = t('common.chatEmptyMessageError')
    return
  }
  isSending.value = true
  errorMessage.value = ''
  try {
    const payload = { role: 'user', content: messageInput.value.trim() }
    const { data } = await createMessage(session.value.session_id, payload)
    messages.value = [...messages.value, data]
    messageInput.value = ''
  } catch (error) {
    errorMessage.value = t('common.chatSendError')
  } finally {
    isSending.value = false
  }
}

const goToSession = () => {
  if (session.value) {
    router.push({ name: 'session-detail', params: { sessionId: session.value.session_id } })
  }
}

watch(
  () => session.value?.session_id,
  async (sessionId) => {
    messages.value = []
    if (sessionId) {
      await loadMessages()
    }
  }
)

watch(
  () => messages.value.length,
  () => {
    scrollToBottom()
  }
)

onMounted(() => {
  if (session.value) {
    loadMessages()
  }
})
</script>
