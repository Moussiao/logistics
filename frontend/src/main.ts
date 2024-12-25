import 'dayjs/locale/ru';
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';

import App from './App.vue';
import router from './router';
import { initTelegramMiniApp } from './utils/telegram';

import './fonts.css';
import './style.css';

// Инициализируем стили на основе данных от Telemgra Mini App
// Ошибку глушим, так как на данном этапе нам она не важна.
initTelegramMiniApp().catch(function () {});

const app = createApp(App);

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
app.use(pinia);

app.use(router);

app.mount('#app');
