<template>
  <div id='app'>
    <h1>My Todo App!</h1>
    <el-input placeholder='Please input' v-model='input'></el-input>
  </div>
</template>

<script>
import { Input } from 'element-ui';

export default {
  components: {
    Input
  }
}
</script>
