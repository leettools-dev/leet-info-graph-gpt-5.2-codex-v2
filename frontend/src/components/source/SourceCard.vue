<template>
  <article class="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
    <div class="flex flex-wrap items-start justify-between gap-3">
      <div class="min-w-0 flex-1">
        <h3 class="truncate text-sm font-semibold text-slate-900">{{ titleText }}</h3>
        <p class="mt-1 text-xs text-slate-500">{{ source.url }}</p>
      </div>
      <span
        class="inline-flex items-center rounded-full bg-slate-100 px-2 py-1 text-xs font-medium text-slate-600"
      >
        {{ confidenceLabel }}
      </span>
    </div>
    <p class="mt-3 text-sm text-slate-600">
      {{ snippetText }}
    </p>
    <div class="mt-4 flex justify-end">
      <a
        class="inline-flex items-center gap-2 text-sm font-medium text-blue-600 hover:text-blue-700"
        :href="source.url"
        target="_blank"
        rel="noopener noreferrer"
        :aria-label="linkAriaLabel"
      >
        {{ t('common.sourceOpenLink') }}
        <span aria-hidden="true">↗</span>
      </a>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  source: {
    type: Object,
    required: true,
  },
})

const { t } = useI18n()

const titleText = computed(() => props.source.title || t('common.sourceUntitled'))
const snippetText = computed(() => props.source.snippet || t('common.sourceNoSnippet'))
const confidenceValue = computed(() => props.source.confidence)

const confidenceLabel = computed(() => {
  if (typeof confidenceValue.value !== 'number') {
    return `${t('common.sourceConfidenceLabel')}: ${t('common.sourceConfidenceUnknown')}`
  }
  return `${t('common.sourceConfidenceLabel')}: ${Math.round(confidenceValue.value * 100)}%`
})

const linkAriaLabel = computed(() => `${t('common.sourceOpenLink')}: ${titleText.value}`)
</script>
