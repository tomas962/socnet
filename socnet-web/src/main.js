import Vue from 'vue'
import App from './App.vue'
import router from './router'
import BootstrapVue from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import vuetify from './plugins/vuetify'

Vue.config.productionTip = false

Vue.use(BootstrapVue)

Vue.prototype.$rest = 'http://192.168.1.72:5000'
Vue.prototype.$loggedIn = false

Vue.mixin({
  
})

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
