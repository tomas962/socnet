<template>
  <div>
    <b-container>
        <h1>Your profile information</h1>
        <b-alert dismissible v-model="showSuccess"> {{success}} </b-alert>
        <b-alert dismissible variant="danger" v-model="showError"> {{error}} </b-alert>
        <b-form @submit="updateProfile">
            <b-row>
                <b-col class="text-right">
                    Username
                </b-col>
                <b-col>
                    <b-form-input type="text" v-model="username"></b-form-input>
                </b-col>
            </b-row>

            <b-row>
                <b-col class="text-right">
                    Age
                </b-col>
                <b-col>
                    <b-form-input type="number" v-model="age"></b-form-input>
                </b-col>
            </b-row>

            <b-row>
                <b-col class="text-right">
                    Group
                </b-col>
                <b-col>
                    <b-form-input disabled type="text" v-model="group"></b-form-input>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                </b-col>
                <b-col cols="2">
                    <b-button type="submit" variant="success">Update profile</b-button>
                </b-col>
                <b-col>
                </b-col>
            </b-row>
                    

        </b-form>
    </b-container>
  </div>
</template>

<script>

export default {
  name: 'Users',
  data: function(){
      return {
          username: '',
          age: '',
          group: '',
          showSuccess: false,
          showError: false,
          error: '',
          success: ''
      }
  },
  created: async function(){
      await this.getUser()
  },

  methods: {
      async getUser(){
          const response = await fetch(this.$rest + '/users/' + this.$root.user_id)
          const json = await response.json()
          this.age = json.age
          this.username = json.username
          this.group = json.group
      },

      async updateProfile(evt){
          evt.preventDefault()
          console.log(this.$data)

          const response = await fetch(this.$rest + '/users/' + this.$root.user_id, {
              method: 'PUT',
              headers: {
                  'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + this.$root.jwttoken
              },
              body: JSON.stringify({username: this.username, age: this.age})
          })

          console.log(response)

          if (response.status == 409){
            this.error = 'Profile update error: ' + response.statusText + '. Username already exists.'
            this.showError = true
          }
          else if (response.status == 204) {
            this.success = 'Profile updated successfuly'
            this.showSuccess = true
            await this.getUser()
          }
          else{
            this.error = 'Profile update error: ' + response.statusText + '. Could not update profile.'
            this.showError = true
          }
      }
  }
}
</script>

<style scoped>
 
</style>