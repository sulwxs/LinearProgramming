<script setup>
import {ref} from "vue";
import LinearProgrammingForm from './components/LinearProgrammingForm.vue'

import MatrixView from "@/components/MatrixView.vue";
import test from "@/components/test.vue";
const fileLists=ref([]);
const handlefileLists=(filelist)=>
{
  fileLists.value=filelist
}
</script>

<template>
  <el-container style="width: 90vmax">
    <el-aside style="width: 50vmax">
      <MatrixView @filelistchange="handlefileLists"></MatrixView>
    </el-aside>

  <el-main style="width: 50vmax">
    <LinearProgrammingForm :file-lists="fileLists"/>
  </el-main>
  </el-container>
<!--  <header>-->

<!--    -->
<!--  </header>-->


</template>

<style>

html,body,#app{
padding-top: 20px;
  height:100%;
  max-width: 100vmax;
}



</style>
