<template>
  <el-container>
    <el-header class="header">
      <div class="header-content">
        <h1 class="title">项目管理</h1>
        <div v-if="selectedProject" class="header-back-button">
          <el-button type="text" @click="selectedProject = null" class="back-button">
            <i class="el-icon-back"></i> 返回列表
          </el-button>
        </div>
      </div>
    </el-header>
    <el-main class="main-content">
      <div class="transition-wrapper">
        <ProjectList
          v-if="!selectedProject"
          :projects="projects"
          @selectProject="selectProject"
          @createProject="createProject"

        />
        <ProjectDetail 
          v-else 
          :project="selectedProject" 
          @back="selectedProject = null"

        />
      </div>
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
const updateProject = (updatedProject) => {
  const index = projects.value.findIndex(p => p.id === updatedProject.id);
  if (index !== -1) {
    projects.value[index] = updatedProject;
    ElMessage.success('项目更新成功');
  }
};
</script>

<style scoped>
.header {
  background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%);
  color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 0 20px;
  border-bottom: 1px solid #eaeaea;
  margin-bottom: 20px;
  height: 60px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.title {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
  letter-spacing: 0.5px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.back-button {
  color: white;
  font-weight: 500;
  opacity: 0.9;
  transition: all 0.2s ease;
}

.back-button:hover {
  opacity: 1;
  transform: translateX(-3px);
}

.main-content {
  padding: 20px;
  background-color: #f8fafc;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  min-height: calc(100vh - 120px);
  transition: all 0.3s ease;
}

.transition-wrapper {
  animation: fadeIn 0.5s ease;
}

/* 项目卡片悬停效果 */
:deep(.project-card) {
  transition: all 0.3s ease;
  border: none;
}

:deep(.project-card:hover) {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

/* 表格美化 */
:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.03);
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

:deep(.el-table th) {
  background-color: #f0f4ff;
  color: #4776E6;
  font-weight: 600;
}

:deep(.el-table--striped .el-table__body tr.el-table__row--striped td) {
  background-color: rgba(71, 118, 230, 0.05);
}

:deep(.el-table__row:hover td) {
  background-color: rgba(142, 84, 233, 0.05) !important;
}

:deep(.el-button) {
  transition: all 0.3s ease;
  border-radius: 6px;
}

:deep(.el-button:not(.back-button):hover) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

:deep(.el-button.gradient-button) {
  font-weight: 500;
  letter-spacing: 0.5px;
}

:deep(.el-divider__text) {
  font-weight: 600;
  color: #4776E6;
  background-color: #f8fafc;
}

:deep(.el-card) {
  transition: all 0.3s ease;
  overflow: visible;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
