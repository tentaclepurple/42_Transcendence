import { createApp, configureCompat } from 'vue'
import { createPinia } from 'pinia'
import VueCookies from 'vue3-cookies'
import App from './App.vue'
import router from './router'
import { BootstrapVue3 } from 'bootstrap-vue-3'
import store from './stores/vuex_store'; 

import { library } from '@fortawesome/fontawesome-svg-core';
import { faUser, faTrophy, faGamepad, faStar } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

//Bootstrap
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css';

const app = createApp(App)

// Configure Vue 3 compat mode globally
configureCompat({
  MODE: 3,
  RENDER_FUNCTION: false,
  COMPONENT_V_MODEL: false
})

app.use(createPinia())
app.use(router)
app.use(VueCookies);
app.use(BootstrapVue3);
app.use(store);
//app.use(IconsPlugin);

// Añadir los iconos a la librería
library.add(faUser, faTrophy, faGamepad, faStar);
app.component('font-awesome-icon', FontAwesomeIcon);

app.mount('#app')
