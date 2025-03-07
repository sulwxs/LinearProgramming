<template>
  <el-card>
    <h2>{{ project.name }}</h2>
    <el-divider>求解问题</el-divider>
    <el-table :data="project.issues" style="width: 100%">
      <el-table-column prop="id" label="ID" width="100"></el-table-column>
      <el-table-column prop="description" label="描述"></el-table-column>
    </el-table>

    <el-divider>文件数据</el-divider>
    <el-table :data="project.files" style="width: 100%">
      <el-table-column prop="id" label="文件ID" width="100"></el-table-column>
      <el-table-column prop="name" label="文件名"></el-table-column>
    </el-table>

    <el-button type="primary" @click="$emit('back')">返回</el-button>
  </el-card>
</template>

<script setup>
import { defineProps } from "vue";

defineProps(["project"]);
</script>
