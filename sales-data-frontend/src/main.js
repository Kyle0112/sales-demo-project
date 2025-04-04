import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import config from './config.json'

const app = createApp(App)
app.use(router)
app.config.globalProperties.$config = config
app.mount('#app')