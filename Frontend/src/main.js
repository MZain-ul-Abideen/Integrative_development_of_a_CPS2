import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './styles/main.css'; // Import your global CSS

createApp(App).use(router).mount('#app')
