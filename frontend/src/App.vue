<script setup>
import {ref} from "vue";
import LinearProgrammingForm from './components/LinearProgrammingForm.vue'

import MatrixView from "@/components/MatrixView.vue";
import test from "@/components/test.vue";
import MatrixTable from "@/components/MatrixTable.vue";
import {CirclePlus, Document, Files, Grid, Setting, Star, UploadFilled} from "@element-plus/icons-vue";
import IconDocumentation from "@/components/icons/IconDocumentation.vue";
const fileLists=ref([]);
const handlefileLists=(filelist)=>
{
  fileLists.value=filelist
}
const show_left_menu=ref(true)
const isCollapse=ref(true)

</script>

<template>

    <el-container class="layout-container-demo" style="height: 100%;">
    <el-aside width="200px">
      <el-image style="width: 100%;height: 50px"></el-image>
      <div>
        <el-scrollbar>
        <el-menu  >
          <el-menu-item index="1">
            <template #title>
              <el-icon><circle-plus/></el-icon>问题求解
            </template>
          </el-menu-item>
          <el-menu-item index="2">
            <template #title>
              <el-icon><grid/></el-icon>矩阵数据
            </template>
          </el-menu-item>
          <el-sub-menu index="3">
            <template #title>
              <el-icon><upload/></el-icon>文件管理
            </template>
          </el-sub-menu>
          <el-sub-menu index="4">
            <template #title>
              <el-icon><files/></el-icon>历史记录
            </template>
          <el-menu-item >问题1</el-menu-item>
          <el-menu-item >问题2</el-menu-item>
          <el-menu-item >问题3</el-menu-item>
          <el-menu-item >问题4</el-menu-item>
          </el-sub-menu>
          <el-menu-item  index="5" class="menu_setting">
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
        <el-scrollbar>
          <el-table :data="tableData">
            <el-table-column prop="date" label="Date" width="140" />
            <el-table-column prop="name" label="Name" width="120" />
            <el-table-column prop="address" label="Address" />
          </el-table>
        </el-scrollbar>
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
