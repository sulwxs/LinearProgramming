<template>
<div style="width: 100%;height: 100%;background:linear-gradient(to right, #6a11cb80, #2575fc80);padding: 0px;margin: 0px;">
   <el-container style="height: 100vh;">
<!--         <el-header style="height: 60px; background-color: rgba(0, 0, 0, 0.1);padding: 0px;margin: 0px;">-->
<!--    -->
<!--    </el-header>-->
   <el-menu
    :default-active="activeIndex"
    :de
    class="el-menu-demo"
    mode="horizontal"
    :ellipsis="false"
    @select="handleSelect"
    justify="space-between"
    background-color="#545c6450"
    text-color="#fff"
    active-text-color="#ffd04b"
  >

    <el-menu-item index="0">
    <img
        style="width: 60px;"
        src="assets/logo.svg"
        alt="Element logo"
      />
    </el-menu-item>
    <el-menu-item index="1">Processing Center</el-menu-item>
    <el-sub-menu index="2" >
      <template #title>{{lang}}</template>
      <el-menu-item  v-for="(lan,idx) in lang_list" :index="'2-'+idx" @click="lang=lan" style="background-color: dodgerblue">{{lan}}</el-menu-item>
<!--      <el-menu-item index="2-2">中文</el-menu-item>-->
<!--      <el-menu-item index="2-3">English</el-menu-item>-->
    </el-sub-menu>
  </el-menu>
 <el-main style="background-color: rgba(0, 0, 0, 0.1); height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 0px;margin: 0px;">
    <div style="text-align: center; color: white;">
      <h1 style="font-size: 3em; font-weight: bold;">欢迎来到主页</h1>
      <el-text style="font-size: 1.2em; margin-top: 10px;color: white;">这是一个简短的主页说明。</el-text>
      <el-row  style="justify-content: center;" wrap>

        <el-card style="margin:15px 15px 15px 15px;width: 250px;" >
          <div slot="header" class="clearfix">
            <span>开始使用</span>
          </div>
          <el-text style="margin-top:10px; ">点击在线使用线性规划求解器</el-text>
        </el-card>
            <el-card style="margin:15px 15px 15px 15px;width: 250px;" >
          <div slot="header" class="clearfix">
            <span>登录</span>
          </div>
          <el-text>登录进行数据保存</el-text>
        </el-card>




      </el-row>
    </div>
  </el-main>
      <el-footer>Footer</el-footer>
    </el-container>

</div>

</template>

<script lang="ts" setup>
import { ref } from 'vue'
const lang='中文'
const lang_list=['中文','English']
const activeIndex = ref('0')
const sub_menu_index=ref('2-1')
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>

<style scoped>
.el-menu--horizontal > .el-menu-item:nth-child(1) {
  margin-right: auto;
}
.el-menu .el-menu--horizontal{
  border: none;
}

</style>
