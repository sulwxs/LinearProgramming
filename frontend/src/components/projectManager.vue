<template>
  <el-container>
    <el-header>
      <h1>项目管理</h1>
    </el-header>
    <el-main>
      <ProjectList
        v-if="!selectedProject"
        :projects="projects"
        @selectProject="selectProject"
        @createProject="createProject"
      />
      <ProjectDetail v-else :project="selectedProject" @back="selectedProject = null" />
    </el-main>
  </el-container>
</template>

<script setup>
import { ref } from "vue";
import ProjectList from "@/components/ProjectList.vue";
import ProjectDetail from "@/components/ProjectDetail.vue";

const projects = ref([
  {
    id: 1,
    name: "AI研究项目",
    issues: [{ id: 101, description: "优化算法问题" }, { id: 102, description: "数据预处理问题" }],
    files: [{ id: 1, name: "data1.csv" }, { id: 2, name: "report.pdf" }],
  },
]);

const selectedProject = ref(null);

const selectProject = (project) => {
  selectedProject.value = project;
};

const createProject = (newProject) => {
  projects.value.push(newProject);
};
</script>
