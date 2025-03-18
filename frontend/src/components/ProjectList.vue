<template>  <!-- 快速开始 -->
  <el-divider>快速开始</el-divider>
  <el-row :gutter="20" style="padding-left: 10px">
    <el-col v-for="example in quickStartExamples" :key="example.id" :span="4">
      <el-card class="quick-start-card" shadow="hover" @click="startQuickProject(example)">
        <h3 class="quick-start-title">{{ example.name }}</h3>
        <p>{{ example.description }}</p>
      </el-card>
    </el-col>
  </el-row>

  <el-row style="margin-bottom: 20px;padding-left: 10px">
     <el-button class="gradient-button" @click="addNewProject" >+ 创建新项目</el-button>
     <el-button class="gradient-button" @click="addNewProject" >多选</el-button>
  </el-row>


  <el-row :gutter="20" style="padding-left: 10px">
    <el-col v-for="project in projects" :key="project.id" :span="4" :gutter="20">
      <el-card class="project-card" shadow="hover" @click="viewProject(project)">
        <h3 class="project-title">{{ project.name }}</h3>
        <p>包含问题数: {{ project.issues.length }}</p>
        <p>文件数量: {{ project.files.length }}</p>
      </el-card>
    </el-col>
  </el-row>


</template>

<script setup>
import { defineProps, defineEmits } from "vue";

defineProps(["projects"]);
const emit = defineEmits(["selectProject", "createProject"]);

const viewProject = (project) => {
  emit("selectProject", project);
};

// 快速开始示例
const quickStartExamples = [
  { id: 1, name: "机器学习项目", description: "包含数据分析和模型训练的示例" },
  { id: 2, name: "Web 开发项目", description: "包含前端和后端结构的模板" },
  { id: 3, name: "自动化脚本", description: "自动化处理任务的示例代码" },
];

const startQuickProject = (example) => {
  const newProject = {
    id: Date.now(),
    name: example.name,
    issues: [],
    files: [],
  };
  emit("createProject", newProject);
};

const addNewProject = () => {
  emit("createProject", { id: Date.now(), name: "新建项目", issues: [], files: [] });
};
</script>

<style scoped>
/* 项目卡片美化 */
.project-card {
  background: linear-gradient(135deg, #2193b0, #6dd5ed);
  color: white;
  border-radius: 10px;
  transition: transform 0.3s ease;
}

.project-card:hover {
  transform: scale(1.05);
}

/* 标题 */
.project-title {
  font-size: 20px;
  font-weight: bold;
}

/* 快速开始卡片 */
.quick-start-card {
  background: linear-gradient(135deg, #ff9966, #ff5e62);
  color: white;
  border-radius: 10px;
  transition: transform 0.3s ease;
}

.quick-start-card:hover {
  transform: scale(1.05);
}

/* 快速开始标题 */
.quick-start-title {
  font-size: 18px;
  font-weight: bold;
}

/* 渐变色按钮 */
.gradient-button {
  background: linear-gradient(90deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 25px;
  font-size: 16px;
  cursor: pointer;
  transition: opacity 0.3s ease;
  margin-top: 20px;
}

.gradient-button:hover {
  opacity: 0.8;
}
</style>
