<template>
    <div>
        <b-card header-bg-variant="success" v-bind:header="comment.user.username + ' | commented at ' + comment.date">
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
    }
}
</script>