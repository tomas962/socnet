<template>
    <div>
        <b-card header-bg-variant="primary" 
        v-bind:header="post.user.username + ' | ' 
        + new Date(post.date).toLocaleDateString('lt', {
            timeZone: 'UTC', day: 'numeric', year: 'numeric',
             month: 'numeric', hour:'numeric', minute:'numeric'})">
            <b-alert v-if="show_error" show variant="danger">Error: {{error}}</b-alert>
            <b-button variant="danger" v-if="this.$root.group == 'admin'" @click="$bvModal.show('modal-'+post.post_id)">Delete Post</b-button>
            <b-modal ok-title="Confirm" @ok="deletePost" v-bind:id="'modal-'+post.post_id" title="Are you sure about this?">
               <p>Do you want to delete this post?</p>
               <p>Post ID: {{post.post_id}}</p>
               <p>User: {{post.user.username}}</p>
               <p>Text: {{post.text}}</p>
            </b-modal>
            <b-card-text >
                {{ post.text }}
            </b-card-text>
            <h4>Comments</h4>
            <b-row>
                <!-- <b-alert dismissible v-model="commentAlert[post.post_id]"> Comment succesfuly deleted </b-alert> -->
                <b-col v-for="comment in post.comments" :key="comment.comment_id">
                    <Comment v-bind:comment="comment"></Comment>
                </b-col>
            </b-row>
        </b-card>
    </div>
</template>

<script>
import Comment from './Comment'
export default {
    name: 'Post',
    props: {
        post: Object
    },
    components: {Comment},
    data: function (){
        return {
            show_error: false,
            error: '',
            // commentAlert: {}
        }
    },
    created: function() {
        // this.commentAlert[this.post.post_id] = false
        // this.$root.$on('comment-deleted', () => {this.commentAlert[this.post.post_id] = true})
    },

    methods:{
        async deletePost(evt){
            const response = await fetch(this.$rest + '/posts/' + this.post.post_id, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.$root.jwttoken
                }
            });
            console.log(response)

            if (response.status !== 200){
                this.error = response.statusText + ". Could not delete post!"
                this.show_error = true
            }
            else{
                this.$emit('post-deleted')
            }
        }
    }
}
</script>