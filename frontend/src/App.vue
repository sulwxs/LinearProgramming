<script setup>

import LinearProgrammingForm from './components/LinearProgrammingForm.vue'

import MatrixView from "@/components/MatrixView.vue";
import test from "@/components/test.vue";
</script>

<template>
  <el-container style="width: 90vmax">
    <el-aside style="width: 50vmax">
      <MatrixView></MatrixView>
    </el-aside>

  <el-main style="width: 50vmax">
    <LinearProgrammingForm />
  </el-main>
  </el-container>
<!--  <header>-->

<!--    -->
<!--  </header>-->


</template>

<style>

html,body,#app{

  height:100%;
  max-width: 100vmax;
}



</style>
