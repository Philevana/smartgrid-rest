<template>
  <el-container class="app-container">
    <el-header class="app-header">
      Smart Grid — Energy Management Platform
    </el-header>
    <el-main class="app-main">
      <Dashboard />
    </el-main>
  </el-container>
</template>

<script>
import Dashboard from './components/Dashboard.vue'
export default { components: { Dashboard } }
</script>

<style>
.app-container {
  min-height: 100vh;
  background-color: #f5f7fa; /* 浅灰背景 */
}
.app-header {
  background: #409eff;
  color: white;
  font-size: 20px;
  padding-left: 20px;
  display: flex;
  align-items: center;
}
.app-main {
  padding: 20px;
}
</style>
