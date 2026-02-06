import { createPinia } from 'pinia'

export const pinia = createPinia()

export * from './modules/app'
export * from './modules/auth'
export * from './modules/session'
