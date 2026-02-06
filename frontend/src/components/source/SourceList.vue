<template>
  <section class="space-y-4 rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
    <header>
      <h2 class="text-lg font-semibold text-slate-900">{{ t('common.sourcesTitle') }}</h2>
      <p class="mt-1 text-sm text-slate-500">{{ t('common.sourcesSubtitle') }}</p>
    </header>

    <div v-if="isLoading" class="text-sm text-slate-500">
      {{ t('common.sourcesLoading') }}
    </div>
    <div v-else-if="!sources.length" class="text-sm text-slate-500">
      {{ t('common.sourcesEmpty') }}
    </div>
    <div v-else class="space-y-3">
      <SourceCard v-for="source in sources" :key="source.source_id" :source="source" />
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

import SourceCard from './SourceCard.vue'

const props = defineProps({
  sources: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const { t } = useI18n()

const sources = computed(() => props.sources)
const isLoading = computed(() => props.loading)
</script>
