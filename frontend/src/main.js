import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// import LVTextarea from 'lightvue/textarea'
// import LvButton from 'lightvue/button';

// createApp(App).use(router).mount('#app')
const app = createApp(App)
app.use(router)
// app.component('LVTextarea', LVTextarea);
// app.component('LvButton', LvButton);
app.mount('#app')
