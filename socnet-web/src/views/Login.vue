<template>
  <div>
    <b-container>
    <b-alert v-if="show_error" show variant="danger">Error: {{error}}</b-alert>
    <h1>Login to your account</h1>
    <b-form @submit="onSubmit">
      <b-row>
        <b-col>
          Username
        </b-col>
        <b-col>
          <b-form-input
          v-model="form.username"
          type="text"
          required
          placeholder="Enter your username"
          ></b-form-input>
        </b-col>
      </b-row>

      <b-row>
        <b-col>
          Password
        </b-col>
        <b-col>
          <b-form-input
          v-model="form.password"
          required
          type="password"
        ></b-form-input>
        </b-col>
      </b-row>

      <b-button type="submit" variant="primary">Login</b-button>
    </b-form>
    </b-container>
  </div>
</template>

<script>
import jwt_decode from 'jwt-decode'

export default {
    name:'Register',
    data() {
      return {
        form: {
          username: '',
          password: ''
        },
        error: '',
        show_error: false
      }
    },
    methods: {
      async onSubmit(evt) {
        evt.preventDefault()
        const data = {
          username: this.form.username,
          password: this.form.password
        }
        const response = await fetch(this.$rest + '/auth', {
          method: 'POST', 
          body: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json'
          }
        });
        if (response.status !== 200) {
          const json = await response.json()
          console.log(json)
          this.show_error = true
          this.error = response.statusText + ": " +  json.error
        }
        else{
          //success, save token and redirect to posts
          const json = await response.json()
          console.log(json)
          localStorage.setItem('jwttoken', json.access_token)
          localStorage.setItem('refreshtoken', json.refresh_token)
          localStorage.setItem('user_id', jwt_decode(json.access_token).identity.user_id)
          localStorage.setItem('username', jwt_decode(json.access_token).identity.username)
          localStorage.setItem('logged_in', "true")
          //this.$loggedIn = true //TODO: fix loggedIn
          this.$root.loggedIn = true
          this.$root.$emit('logged-in')
          this.$router.push('/posts')
        }
      }
    }
  }
</script>
