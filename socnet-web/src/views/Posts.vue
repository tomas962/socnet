<template>
  <div>
    <h1 v-on:click="change">User Posts {{this.$root.globalvar}} </h1>
    <b-container>
        <b-alert v-model="showPostDeletedAlert" dismissible>
          Post deleted succesfuly
        </b-alert>
        <div>
          <b-button v-if="this.$root.loggedIn" v-b-modal.modal-1>New Post!</b-button>
            <b-modal ok-title="Post" @ok="onSubmit" id="modal-1" title="Say something!">
                <b-form-group
                  id="input-group-1"
                  label="Post text:"
                  label-for="input-1"
                  description="Share something with others!"
                >
                <b-form-input
                  id="input-1"
                  v-model="posttext"
                  type="text"
                  required
                  placeholder="Enter your post"
                ></b-form-input>
                </b-form-group>
            </b-modal>
        </div>
        <b-row v-for="post in posts" :key="post.post_id">
            <b-col>
               <Post class="post" v-on:post-deleted="onPostDeleted" v-bind:post="post"></Post>
            </b-col>
            <b-col v-if="$root.loggedIn" cols="3">
              <b-form @submit="onSubmitComment">
                <b-form-input
                  class="mt-5"
                  v-model="comments[post.post_id]"
                  type="text"
                  required
                  placeholder="Enter your comment"
                ></b-form-input>
                <b-button class="mt-1" type="submit" v-bind:value="post.post_id" variant="primary">Comment</b-button>
              </b-form>
            </b-col>
        </b-row>
    </b-container>
  </div>
</template>

<script>
import Post from '../components/Post'

export default {
  name: 'Posts',
  components: {Post},
  data: function(){
      return {
        posts:[
          
        ],
        posttext: '',
        comments:{},
        loggedin: localStorage.getItem('logged_in') == 'true',
        glob: this.$root.globalvar,
        showPostDeletedAlert: false
      }
  },
  created: async function(){
    console.log(this.$root)
    this.$root.$on('comment-deleted', async () => {await this.getPosts()})
    await this.getPosts()
  },

  mounted: function () {
  },

  methods: {
      async onSubmit(evt) {
        console.log(evt)
        console.log(this.user_id)
        const response = await fetch(this.$rest + '/users/' + localStorage.getItem('user_id') + '/posts/', {
          method: 'POST', 
          body: JSON.stringify({text: this.posttext}),
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('jwttoken')
          }
        });
        await this.getPosts()
        console.log(response)
      },
      change(){
        this.$root.globalvar = 'changed'
        console.log(this)
      },
      async onSubmitComment(evt) {
        evt.preventDefault()
        console.log(evt)
        const post_id = evt.srcElement[1].value
        const user_id = localStorage.getItem('user_id')
        console.log(this)
        const response = await fetch(`${this.$rest}/posts/${post_id}/users/${user_id}/comments/`, {
          method: 'POST', 
          body: JSON.stringify({text: this.comments[post_id]}),
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('jwttoken')
          }
        });
        await this.getPosts()
        console.log(response)
      },
      
      async getPosts() {
        console.log("MOUNTED")
        const postsReq = fetch(this.$rest + '/posts')
        const usersReq = fetch(this.$rest + '/users')
        const commentsReq = fetch(this.$rest + '/comments')

        let postsJson = await (await postsReq).json()
        let usersJson = await (await usersReq).json()
        let commentsJson = await (await commentsReq).json()
        
        for (let i = 0; i < postsJson.length; i++){
            postsJson[i].user = usersJson.find(user => user.user_id == postsJson[i].user_id)
            postsJson[i].comments = commentsJson.filter(comment => comment.post_id == postsJson[i].post_id)

            for (let j = 0; j < postsJson[i].comments.length; j++){
                postsJson[i].comments[j].user = usersJson.find(user => user.user_id == postsJson[i].comments[j].user_id)
            }
        }
          
        this.posts = postsJson
        console.log(this.posts)
      },

      async onPostDeleted(){
        await this.getPosts()
        this.showPostDeletedAlert=true
      }
      
  }
}
</script>

<style scoped>
 
</style>