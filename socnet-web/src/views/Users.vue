<template>
  <div>
    <b-container>
        <h1>Manage Users</h1>
        <b-alert dismissible v-model="showSuccess"> {{success}} </b-alert>
        <b-alert dismissible variant="danger" v-model="showError"> {{error}} </b-alert>
        <b-table striped hover :items="users"></b-table>
        <b-row>
            <b-col></b-col>
            <b-col cols="2">
                <b-form @submit="onSubmitDelete">
                    <h4>Delete user</h4>
                    <b-form-group
                        label-for="uid"
                        description="Enter user ID"
                    >
                        <b-form-input
                        id="uid"
                        v-model="userid"
                        type="number"
                        required
                        placeholder="User ID"
                        ></b-form-input>
                    </b-form-group>
                    <b-button type="submit" variant="danger">Delete</b-button>
                </b-form>
            </b-col>
            <b-col></b-col>
        </b-row>

        <b-row class="mt-5">
            <b-col></b-col>
            <b-col cols="2">
                <b-form @submit="onSubmitGroup">
                    <h4>Change user group</h4>
                    <b-form-group
                        label-for="ugrp"
                        description="Enter user ID"
                    >
                        <b-form-input
                        id="ugrp"
                        v-model="userid_for_group"
                        type="number"
                        required
                        placeholder="User ID"
                        ></b-form-input>

                        
                    </b-form-group>
                    <b-form-select class="mt-2 mb-2"
                        v-model="group"
                        :options="groups"
                        required
                    ></b-form-select>
                    <b-button type="submit" variant="danger">Change group</b-button>
                </b-form>
            </b-col>
            <b-col></b-col>
        </b-row>
    </b-container>
  </div>
</template>

<script>

export default {
  name: 'Users',
  data: function(){
      return {
        users: [],
        userid: 0,
        userid_for_group: 0,
        showSuccess: false,
        showError: false,
        error: '',
        success: '',
        groups: [{ text: 'Select Group', value: null }, 'admin', 'regular'],
        group: null
      }
  },
  created: async function(){
      await this.getUsers()
  },

  methods: {
      async getUsers(){
          const response = await fetch(this.$rest + '/users')
          const json = await response.json()
          this.users = json
      },

      async onSubmitDelete(evt){
          evt.preventDefault()
          console.log(this.userid)
          const response = await fetch(this.$rest + '/users/' + this.userid, {
              method: 'DELETE',
              headers:{
                  'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + this.$root.jwttoken
              }
          })

          console.log(response)
          if(response.status == 200){
              this.success = "User deleted successfuly"
              this.showSuccess = true
              this.getUsers()
          }else{
              this.error = 'User delete error ' + response.statusText + '. Could not delete user'
              this.showError = true
          }
      },

      async onSubmitGroup(evt){
          evt.preventDefault()

          console.log(this.userid_for_group)
          console.log(this.group)

          const response = await fetch(this.$rest + '/users/' + this.userid_for_group, {
              method: 'PUT',
              headers: {
                  'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + this.$root.jwttoken
              },
              body: JSON.stringify({group: this.group})
          })

          if (response.status == 204){
              this.success = "User group changed successfuly"
              this.showSuccess = true
              this.getUsers()
          }
          else{
              this.error = 'User group change error ' + response.statusText + '. Could not change user group'
              this.showError = true
          }
          console.log(response)
      }
  }
}
</script>

<style scoped>
 
</style>