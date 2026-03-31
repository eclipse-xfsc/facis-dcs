import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import { router } from './router/router'
import { useErrorStore } from './stores/error-store'

const app = createApp(App).use(createPinia()).use(router)

const errorStore = useErrorStore()

app.config.errorHandler = (err, instance, info) => {
    const message = err instanceof Error ? err.message : `Error: ${err ? String(err) : 'unknown'}`
    errorStore.add(message)
}

window.addEventListener('unhandledrejection', event => {
    errorStore.add(event.reason)
})

app.mount('#app')
