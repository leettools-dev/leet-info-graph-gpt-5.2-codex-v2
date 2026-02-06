import { createI18n } from 'vue-i18n'
import en from './en'
import ja from './ja'
import zh from './zh'

const messages = { en, ja, zh }

export const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages,
})
