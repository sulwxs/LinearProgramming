<script setup>
import {ref} from "vue";
import LinearProgrammingForm from './components/LinearProgrammingForm.vue'

import MatrixView from "@/components/MatrixView.vue";
import test from "@/components/test.vue";
import MatrixTable from "@/components/MatrixTable.vue";
import {CirclePlus, Document, Files, Grid, Setting, Star, UploadFilled} from "@element-plus/icons-vue";
import IconDocumentation from "@/components/icons/IconDocumentation.vue";
import router from "../router/router";
import axios from "axios";
import {ElMessage} from "element-plus";
const fileLists=ref([]);
const handlefileLists=(filelist)=>
{
  fileLists.value=filelist
}
const handleOpen = (key, keyPath)=>
{
  console.log(key)

// router.path='/upload'
}
const handleClose = (key, keyPath)=>
{

}
const show_left_menu=ref(true)
const isCollapse=ref(true)

const loadFileNames = (files) => {
  fileLists.value = files;
  loadallMatx();

};
const handleDeleteFile=(filename)=>
{
  fileLists.value=fileLists.value.filter(f=>f.name!==filename)
   // emits('filelistchange',fileLists.value)
}
const handleFileUpload=(file)=>
{
  let f=fileLists.value.find(i=>i.name===file.name)
  if(f===undefined){
    const nf={name:file.name,status:"success",progress:100,read:false,show:false,open:false}
    fileLists.value.push(nf)}
  else {
    readFile(file.name)
  }
 // emits('filelistchange',fileLists.value)
}
const readFile = async (filename) => {
  // loading.value = true;
  try {
    const response = await axios.get(`http://127.0.0.1:5000/read_csv_matrix?filename=${filename}`);
    if (response.data.matrix) {
      var a = fileLists.value.find(item => item.name === filename);
      a.mat = response.data.matrix;
      a.read = true;
    } else {
      ElMessage.error('读取失败');
      a.read=false;
    }
  } catch (error) {
    console.error('读取文件时发生错误', error);
    ElMessage.error('读取失败');
      a.read=false;

  }
  // loading.value = false;
};
const loadallMatx = async () => {
  // loading.value = true;
  try {

    for (let file of fileLists.value) {
      if (file.read === false) {
        await readFile(file.name);
      }
    }
     // emits('filelistchange',fileLists.value)
  } catch (error) {
    console.log(error)
  }
  // loading.value = false;
};
</script>

<template>

    <el-container class="layout-container-demo" style="height: 100%;">
    <el-aside width="200px">
      <el-image style="width: 100%;height: 50px"></el-image>
      <div>
        <el-scrollbar>
        <el-menu  :router="true" :unique-opened="true" default-active="solver">
          <el-menu-item index="solver">
            <template #title>
              <el-icon><circle-plus/></el-icon>问题求解
            </template>
          </el-menu-item>
          <el-menu-item index="matrixview">
            <template #title>
              <el-icon><grid/></el-icon>矩阵数据
            </template>
          </el-menu-item>
          <el-menu-item index="fileManage" >
            <template #title>
              <el-icon><upload/></el-icon>文件管理
            </template>
          </el-menu-item>
          <el-menu-item index="history">
            <template #title>
              <el-icon><files/></el-icon>历史记录
            </template>
<!--          <el-menu-item route="upload" index="upload">问题1</el-menu-item>-->
<!--          <el-menu-item >问题2</el-menu-item>-->
<!--          <el-menu-item >问题3</el-menu-item>-->
<!--          <el-menu-item >问题4</el-menu-item>-->
          </el-menu-item>
          <el-menu-item  index="setting" class="menu_setting">
                      <template #title>
              <el-icon><setting /></el-icon>设置
            </template>
          </el-menu-item>
        </el-menu>
      </el-scrollbar>
      </div>
    </el-aside>

    <el-container>
      <el-header style="display: flex;justify-content: space-between; font-size: 12px">
        <div class="toolbar">
            <el-button icon="menu" circle></el-button>
            <el-text></el-text>
        </div>
        <div class="toolbar">

          <el-dropdown>
            <el-icon style="margin-right: 8px; margin-top: 1px">
              <setting />
            </el-icon>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>View</el-dropdown-item>
                <el-dropdown-item>Add</el-dropdown-item>
                <el-dropdown-item>Delete</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          <span>Tom</span>
        </div>
      </el-header>

      <el-main>
<!--        <el-scrollbar>-->
<!--          <el-table :data="tableData">-->
<!--            <el-table-column prop="date" label="Date" width="140" />-->
<!--            <el-table-column prop="name" label="Name" width="120" />-->
<!--            <el-table-column prop="address" label="Address" />-->
<!--          </el-table>-->
<!--        </el-scrollbar>-->
        <router-view ref="router_view" :fileLists="fileLists" @loadfilenames="loadFileNames" @filedelete="handleDeleteFile" @fileupload="handleFileUpload"></router-view>
      </el-main>
    </el-container>
  </el-container>
<!--  <el-container style="width: 90vmax">-->
<!--    <el-aside style="width: 50vmax">-->
<!--      <MatrixView @filelistchange="handlefileLists"></MatrixView>-->
<!--&lt;!&ndash;      <MatrixTable></MatrixTable>&ndash;&gt;-->
<!--    </el-aside>-->

<!--  <el-main style="width: 50vmax">-->
<!--    <LinearProgrammingForm :file-lists="fileLists"/>-->
<!--  </el-main>-->
<!--  </el-container>-->
<!--&lt;!&ndash;  <header>&ndash;&gt;-->

<!--&lt;!&ndash;    &ndash;&gt;-->
<!--&lt;!&ndash;  </header>&ndash;&gt;-->


</template>

<style>

html,body,#app{
padding-top: 20px;
  height:100%;
  width: 100%;
  padding:0 0 0 0;

  margin: 0 0 0 0;
}

.layout-container-demo .el-menu {
  border-right: none;
}
.layout-container-demo .el-main {
  padding: 0;
}
.layout-container-demo .toolbar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  right: 20px;
}


</style>
