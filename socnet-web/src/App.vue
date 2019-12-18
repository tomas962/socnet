<template>
  <div id="app">
    <div id="content">
    <Navbar ></Navbar>
    <router-view/>
    </div>
    <!-- <v-card id="footer" height="150"> -->
      <v-footer id="footer"
        absolute
        class="font-weight-medium"
      >
        <v-col
          class="text-center"
          cols="12"
        >
          {{ new Date().getFullYear() }} — <strong class="myfont"> SocNet, Tomas Cizauskas</strong>
        </v-col>
      </v-footer>
    <!-- </v-card> -->
  </div>
</template>

<script>

import Navbar from './components/Navbar'

export default {
  name: 'App',
  components: {
    Navbar
  },
}

</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  position: relative;
  min-height: 100vh;
}

.myfont {
  font-family: 'Girassol', cursive;

}

#content {
  padding-bottom: 2.5rem;    /* Footer height */
}

#footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 2.5rem;            /* Footer height */
}

</style>