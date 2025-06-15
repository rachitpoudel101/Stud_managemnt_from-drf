import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import './assets/main.css';

// axios.defaults.baseURL = 'http://localhost:8000/api/';

// app.config.globalProperties.$axios = axios;
 // Adjust the base URL as needed
createApp(App).use(router).mount('#app');
