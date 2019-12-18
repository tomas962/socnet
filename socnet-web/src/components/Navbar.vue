<template>
  <div id="navbar">
    <b-navbar pills toggleable="lg" type="dark" variant="success">
    <b-navbar-brand href="/"><img src="/img/socnet_logo.png" id="logoimg"></b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item to="/">Main Page</b-nav-item>
        <b-nav-item to="/posts">Posts</b-nav-item>
        <b-nav-item v-if="this.$root.group == 'admin'" to="/users">Manage Users</b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item v-if="!this.$root.loggedIn" to="/login">Login</b-nav-item>
        <b-nav-item v-if="!this.$root.loggedIn" to="/register">Register</b-nav-item>
        <b-nav-item ></b-nav-item>
        <b-nav-item ></b-nav-item>
        <b-nav-item ></b-nav-item>
        <b-nav-text>Welcome, {{this.$root.username}}!</b-nav-text>
        <b-nav-item v-if="this.$root.loggedIn" to="/profile">My Profile</b-nav-item>
        <b-nav-item v-if="this.$root.loggedIn" v-on:click="logOut">Sign Out</b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
  </div>
</template>

<script>
import jwt_decode from 'jwt-decode'

export default {
  name: 'Navbar',

  methods: {
    logOut: function(/*event*/) {
      localStorage.setItem('logged_in', 'false')
      localStorage.removeItem('jwttoken')
      localStorage.removeItem('username')
      localStorage.removeItem('user_id')
      localStorage.removeItem('group')
      //this.$root.$emit('logged-out')
      this.$root.loggedIn = false
      this.$root.username = "Guest"
      this.$root.user_id = -1
      this.$root.group = 'guest'
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
  #logoimg {
    height: 50px;
  }
</style>