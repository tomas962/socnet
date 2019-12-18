<template>
    <div>
        <b-card header-bg-variant="success" v-bind:header="comment.user.username + ' | ' + 
        new Date(comment.date).toLocaleDateString('lt', {
            timeZone: 'UTC', day: 'numeric', year: 'numeric',
             month: 'numeric', hour:'numeric', minute:'numeric'})">
            <b-button variant="danger" v-if="this.$root.group == 'admin'" @click="$bvModal.show('comment-modal-'+comment.comment_id)">Delete Comment</b-button>
            <b-modal ok-title="Confirm" @ok="deleteComment" v-bind:id="'comment-modal-'+comment.comment_id" title="Are you sure about this?">
               <p>Do you want to delete this comment?</p>
               <p>Comment ID: {{comment.comment_id}}</p>
               <p>User: {{comment.user.username}}</p>
               <p>Text: {{comment.text}}</p>
            </b-modal>
            <b-card-text >
                {{ comment.text }}
            </b-card-text>
        </b-card>
    </div>
</template>

<script>
export default {
    name: 'Comment',
    props:{
        comment: Object
    },

    methods: {
        async deleteComment(){
            console.log('DEL COMMENT ' + this.comment.comment_id)
            const request = fetch(this.$rest + '/comments/' + this.comment.comment_id, {
                method: 'DELETE',
                headers:{
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.$root.jwttoken
                }
            })
            const response = await request
            this.$root.$emit('comment-deleted')
        }
    }
}
</script>