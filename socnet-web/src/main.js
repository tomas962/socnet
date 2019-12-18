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

export const globalStore = new Vue({
  data: {
    loggedIn: false
  }
})


new Vue({
  router,
  vuetify,
  render: h => h(App),
  data:{
    loggedIn: localStorage.getItem('jwttoken') != null ? true : false,
    user_id: localStorage.getItem('user_id'),
    username: localStorage.getItem('username') != null ? localStorage.getItem('username') : 'Guest'
  }
}).$mount('#app')
