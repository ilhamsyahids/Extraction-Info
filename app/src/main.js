import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faLinkedin } from '@fortawesome/free-brands-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Install BootstrapVue
Vue.use(BootstrapVue)
Vue.component('font-awesome-icon', FontAwesomeIcon)
library.add(faLinkedin)
Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
