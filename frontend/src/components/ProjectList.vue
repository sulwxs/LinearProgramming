<template>
  <div class="container">
    <!-- 快速开始 -->
    <div class="section-header">
      <h2>快速开始</h2>
      <div class="button-group">
        <el-button class="gradient-button" @click="addNewProject">+ 新建项目</el-button>
      </div>
    </div>
    
    <el-row :gutter="20" class="quick-start-row">
      <el-col 
        v-for="example in quickStartExamples" 
        :key="example.id" 
        :xs="24" :sm="12" :md="8"
      >
        <el-card 
          class="quick-start-card" 
          shadow="hover" 
          @click="startQuickProject(example)"
        >
          <div class="card-content">
            <h3 class="quick-start-title">{{ example.name }}</h3>
            <el-text class="description">{{ example.description }}</el-text>
            <div class="hover-indicator"></div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 我的项目 -->
    <div class="section-header">
      <h2>我的项目</h2>
      <el-text class="counter" type="info">(共{{ projects.length }}个)</el-text>
    </div>

    <el-row :gutter="20" class="project-row">
      <el-col 
        v-for="project in projects" 
        :key="project.id" 
        :xs="24" :sm="12" :md="8" :lg="6"
      >
        <el-card 
          class="project-card" 
          shadow="hover" 
          @click="viewProject(project)"
        >
          <div class="card-content">
            <div class="card-header">
              <h3 class="project-title">{{ project.name }}</h3>
              <el-tag 
                v-if="project.issues.length > 0" 
                type="warning" 
                size="small"
              >
                {{ project.issues.length }}个问题
              </el-tag>
            </div>
            
            <div class="stats">
              <div class="stat-item">
                <el-icon><Document /></el-icon>
                <span>{{ project.files.length }} 文件</span>
              </div>
              <div class="stat-item">
                <el-icon><Clock /></el-icon>
                <span>{{ formatDate(project.createdAt) }}</span>
              </div>
            </div>
            
            <div class="hover-indicator"></div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";
import { Document, Clock } from '@element-plus/icons-vue';
defineProps(["projects"]);
const emit = defineEmits(["selectProject", "createProject"]);

const viewProject = (project) => {
  emit("selectProject", project);
};

// 快速开始示例
const quickStartExamples = [
  { id: 1, name: "机器学习项目", description: "" },
  { id: 2, name: "工程自动化项目", description: "" },
  { id: 3, name: "金融与投资项目", description: "" },
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
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
};
</script>

<style scoped>
.container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 40px 0 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--el-border-color);
}

.section-header h2 {
  margin: 0;
  font-size: 20px;
  color: var(--el-text-color-primary);
}

.counter {
  font-size: 14px;
}

/* 卡片通用样式 */
.quick-start-card,
.project-card {
  height: 180px;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  margin-bottom: 20px;
}

.quick-start-card {
  background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
}

.project-card {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
}

.card-content {
  height: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  z-index: 2;
}

/* 标题样式 */
.quick-start-title {
  font-size: 18px;
  color: #fff;
  margin: 0 0 12px;
  text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.project-title {
  font-size: 16px;
  color: var(--el-text-color-primary);
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 统计信息 */
.stats {
  display: flex;
  gap: 15px;
  margin-top: auto;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--el-text-color-secondary);
}

/* 悬停效果 */
.hover-indicator {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255,255,255,0.1);
  opacity: 0;
  transition: opacity 0.3s;
}

.quick-start-card:hover .hover-indicator,
.project-card:hover .hover-indicator {
  opacity: 1;
}

/* 按钮样式优化 */
.gradient-button {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white !important;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  transition: transform 0.2s;
}

.gradient-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .quick-start-card,
  .project-card {
    height: 160px;
  }
  
  .card-content {
    padding: 15px;
  }
  
  .quick-start-title {
    font-size: 16px;
  }
  
  .project-title {
    font-size: 14px;
  }
}
</style>
