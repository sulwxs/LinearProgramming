<template>
  <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    :ellipsis="false"
    @select="handleSelect"
  >
    <el-menu-item index="0">
      <img
        style="width: 90px;"
        src="./assets/logo.svg"
        alt="Element logo"
      />
    </el-menu-item>
    <el-menu-item index="1">Processing Center</el-menu-item>
    <el-sub-menu index="2" >
      <template #title>语言</template>
      <el-menu-item index="2-2">中文</el-menu-item>
      <el-menu-item index="2-3">English</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const activeIndex = ref('1')
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>

<style scoped>
.el-menu--horizontal > .el-menu-item:nth-child(1) {
  margin-right: auto;
}
</style>
