<template>
  <div id="navbar">
    <b-navbar pills toggleable="lg" type="dark" variant="success">
    <b-navbar-brand href="/">Soc Net</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item to="/">Main Page</b-nav-item>
        <b-nav-item to="/posts">Posts</b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item v-if="!loggedin" to="/login">Login</b-nav-item>
        <b-nav-item v-if="!loggedin" to="/register">Register</b-nav-item>
        <b-nav-item ></b-nav-item>
        <b-nav-item ></b-nav-item>
        <b-nav-item ></b-nav-item>
        <b-nav-text>Welcome, {{username}}!</b-nav-text>
        <b-nav-item v-if="loggedin" to="/profile">My Profile</b-nav-item>
        <b-nav-item v-if="loggedin" v-on:click="logOut">Sign Out</b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
  </div>
</template>

<script>
import jwt_decode from 'jwt-decode'

export default {
  name: 'Navbar',

  data: function(){
    //let now = new Date() / 1000;
    let token = localStorage.getItem('jwttoken')
    let jwt = null
    if (token !== null)
      jwt = jwt_decode(token)
    
    //TODO: make reactive
    return {
      username: jwt !== null ? jwt.identity.username : 'Guest',
      loggedin: localStorage.getItem('logged_in') == 'true'
    }
  },

  methods: {
    logOut: function(/*event*/) {
      localStorage.setItem('logged_in', 'false')
      localStorage.removeItem('jwttoken')
      this.loggedin = false
      this.username = "Guest"
      this.$root.$emit('logged-out')
      this.$router.push('/')
    }
  },

  created: function () {
    this.$root.$on('logged-in',  () => {
      console.log('logged-in on')
      this.loggedin = true
      this.username = localStorage.getItem('username')
      console.log(this)
    }) 
  }
}
</script>

