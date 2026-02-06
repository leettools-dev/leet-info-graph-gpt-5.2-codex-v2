<template>
  <section class="rounded-lg border bg-white p-6 shadow-sm">
    <h1 class="text-xl font-semibold">{{ t('common.loginTitle') }}</h1>
    <p class="mt-2 text-sm text-gray-500">{{ t('common.loginPrompt') }}</p>
    <div class="mt-4 flex items-center gap-3">
      <div ref="googleButtonRef"></div>
      <el-button
        type="primary"
        :loading="authStore.status === 'loading'"
        :disabled="!isReady"
        :aria-label="t('common.loginButton')"
        @click="prompt"
      >
        {{ t('common.loginButton') }}
      </el-button>
    </div>
    <p v-if="authStore.error" class="mt-3 text-sm text-red-600">
      {{ authStore.error?.message || t('common.authFailed') }}
    </p>
    <p v-if="googleError" class="mt-3 text-sm text-red-600">
      {{ t('common.googleUnavailable') }}
    </p>
  </section>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '../../stores/modules/auth'
import { useGoogleAuth } from '../../composables/useGoogleAuth'

const authStore = useAuthStore()
const router = useRouter()
const { t } = useI18n()
const googleButtonRef = ref(null)

const { isReady, error: googleError, renderButton, prompt } = useGoogleAuth()

const renderGoogle = () => {
  if (googleButtonRef.value) {
    renderButton(googleButtonRef.value)
  }
}

onMounted(renderGoogle)
watch(isReady, (ready) => {
  if (ready) {
    renderGoogle()
  }
})
watch(
  () => authStore.isAuthenticated,
  (isAuthenticated) => {
    if (isAuthenticated) {
      router.push({ name: 'chat' })
    }
  },
  { immediate: true }
)
</script>
