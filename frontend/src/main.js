import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// import LVTextarea from 'lightvue/textarea'
// import LvButton from 'lightvue/button';
// import LvDropdown from 'lightvue/dropdown';
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

// createApp(App).use(router).mount('#app')
const app = createApp(App)
app.use(router)
app.component('Datepicker', Datepicker);
// app.component('LvDropdown', LvDropdown);
// app.component('LVTextarea', LVTextarea);
// app.component('LvButton', LvButton);
app.mount('#app')
