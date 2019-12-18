<template>
    <div>
        <b-card header-bg-variant="primary" v-bind:header="post.user.username + ' | posted at ' + post.date">
            <b-card-text >
                {{ post.text }}
            </b-card-text>
            <h4>Comments</h4>
            <b-row>
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
    components: {Comment}
}
</script>