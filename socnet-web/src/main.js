import Vue from 'vue'
import App from './App.vue'
import router from './router'
import BootstrapVue from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import vuetify from './plugins/vuetify'
import jwt_decode from 'jwt-decode'

Vue.config.productionTip = false

Vue.use(BootstrapVue)

Vue.prototype.$rest = 'http://192.168.1.66:5000'
Vue.prototype.$loggedIn = false

export const globalStore = new Vue({
  data: {
    loggedIn: false
  }
})

let jwt = localStorage.getItem('jwttoken')
let decoded_jwt = {}
let user_logged_in = false

if (jwt != null){
  let now = new Date() / 1000;
  decoded_jwt = jwt_decode(jwt)
  user_logged_in = decoded_jwt.exp > now
}


var app = new Vue({
  router,
  vuetify,
  render: h => h(App),
  data:{
    loggedIn:  user_logged_in,
    user_id: user_logged_in ? localStorage.getItem('user_id') : -1,
    username: user_logged_in ? localStorage.getItem('username') : 'Guest',
    group: user_logged_in ? localStorage.getItem('group') : 'guest',
    jwttoken: user_logged_in ? localStorage.getItem('jwttoken') : null
  }
}).$mount('#app')

//console.log(app)