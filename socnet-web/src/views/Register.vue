<template>
  <div>
    <b-container>
    <b-alert v-if="show_error" show variant="danger">Error: {{error}}</b-alert>
    <h1>Register new account</h1>
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
          Your Age
        </b-col>
        <b-col>
          <b-form-input
          v-model="form.age"
          type="number"
          required
          placeholder="Enter your age"
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

      <b-row>
        <b-col>
          Confirm Password
        </b-col>
        <b-col>
          <b-form-input
          v-model="form.confirm_password"
          required
          type="password"
        ></b-form-input>
        </b-col>
      </b-row>


      <b-button type="submit" variant="primary">Register</b-button>
    </b-form>
    </b-container>
  </div>
</template>

<script>

export default {
    name:'Register',
    data() {
      return {
        form: {
          username: '',
          password: '',
          confirm_password: '',
          age: 0
        },
        error: '',
        show_error: false
      }
    },
    methods: {
      async onSubmit(evt) {
        evt.preventDefault()
        console.log(this)
        const data = {
          username: this.form.username,
          age: this.form.age,
          password: this.form.password
        }
        //TODO: add password validation
        const response = await fetch(this.$rest + '/users/', {
          method: 'POST', 
          body: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json'
          }
        });
        if (response.status !== 201) {
          if (response.status === 409) {
            this.show_error = true
            this.error = response.statusText + ": Username already exists"
          }
        }
        else{
          //success, redirect to login
          this.$router.push('/login')
        }
      }
    }
  }
</script>
