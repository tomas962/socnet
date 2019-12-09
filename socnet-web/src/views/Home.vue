<template>
  <div class="home">
    <h1>Welcome to SocNet</h1>
    <el-row>
      <el-col>
        <router-link to="login"><el-button type="success" round>Login</el-button></router-link>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <router-link to="register"><el-button type="primary" round>Register new account</el-button></router-link>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <router-link to="home"><el-button type="warning" round>Browse as a guest</el-button></router-link>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import {Button, Col, Row} from 'element-ui'

export default {
  name: 'home',
  components: {
    Button
  }
}
</script>

<style scoped>
 .el-row {
   margin-bottom: 10px;
 }
</style>