<template>
  <el-card class="project-detail">
    <!-- 头部操作区 -->
    <div class="header-actions">
      <el-button type="primary" @click="handleEdit" :icon="Edit" circle />
      <el-button type="danger" @click="confirmDelete" :icon="Delete" circle />
      <el-button type="info" @click="$emit('back')" :icon="Back" circle />
      <el-button 
        type="info" 
        @click="$emit('back')" 
        :icon="Back"
        class="text-button"
        style="margin-left: auto;"
      >
        返回列表
      </el-button>   
    </div>

    <!-- 项目信息编辑区 -->
    <el-form :model="form" v-if="isEditing" class="edit-form">
      <el-form-item label="项目名称" prop="name"
        :rules="[{ required: true, message: '项目名称不能为空' }]">
        <el-input v-model="form.name" />
      </el-form-item>
      
      <el-form-item label="项目描述">
        <el-input v-model="form.description" type="textarea" :rows="3" />
      </el-form-item>

      <div class="form-actions">
        <el-button type="success" @click="saveEdit" :icon="Check" circle />
        <el-button @click="cancelEdit" :icon="Close" circle />
      </div>
    </el-form>

    <!-- 项目信息展示区 -->
    <div v-else class="project-info">
      <h2 class="project-name">{{ project.name }}</h2>
      <el-text v-if="project.description" type="info" class="description">
        {{ project.description }}
      </el-text>
      
    </div>

    <!-- 问题管理 -->
    <el-divider>
      <span class="section-title">求解问题</span>
      <el-button type="primary" @click="showIssueDialog('create')" :icon="Plus" circle />
    </el-divider>
    
    <el-table :data="project.issues" highlight-current-row>
      <el-table-column prop="id" label="ID" width="100" />
      <el-table-column prop="description" label="问题描述">
        <template #default="{ row }">
          <div class="issue-item">
            <el-text v-if="row.resolved" type="success" class="status-tag">
              <el-icon><SuccessFilled /></el-icon>
            </el-text>
            <el-text :type="row.resolved ? 'success' : 'danger'">
              {{ row.description }}
            </el-text>
            <el-tag v-if="row.priority" :type="priorityType(row.priority)" effect="light">
              优先级 {{ row.priority }}
            </el-tag>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="{ row }">
          <el-button type="primary" @click="showIssueDialog('edit', row)" :icon="Edit" link />
          <el-button type="danger" @click="deleteIssue(row.id)" :icon="Delete" link />
        </template>
      </el-table-column>
    </el-table>

    <!-- 文件管理 -->
    <el-divider>
      <div class="file-divider">
        <span class="section-title">知识库文件</span>
        <el-upload
          :before-upload="handleUpload"
          :show-file-list="false"
          :on-progress="handleUploadProgress"
        >
          <el-button type="primary" :icon="Upload" circle />
        </el-upload>
      </div>
    </el-divider>
    
    <el-table :data="project.files">
      <el-table-column prop="name" label="文件名">
        <template #default="{ row }">
          <div class="file-item">
            <el-icon class="file-icon">
              <Document />
            </el-icon>
            <el-text class="file-name">{{ row.name }}</el-text>
            <el-tag v-if="row.size" size="small">{{ row.size }}</el-tag>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button type="primary" @click="downloadFile(row)" :icon="Download" link />
          <el-button type="danger" @click="deleteFile(row.id)" :icon="Delete" link />
        </template>
      </el-table-column>
    </el-table>

    <!-- 问题编辑对话框 -->
    <el-dialog v-model="issueDialog.visible" :title="`${issueDialog.mode === 'create' ? '新建' : '编辑'}问题描述`">
      <el-form :model="issueDialog.form">
        <el-form-item label="问题描述" required>
          <el-input v-model="issueDialog.form.description" />
        </el-form-item>
        <el-form-item label="ID" required>
          <el-input v-model="issueDialog.form.id" />
        </el-form-item>
        <el-form-item label="优先级">
          <el-rate 
            v-model="issueDialog.form.priority"
            :max="3"
            :allow-half="false"
            show-text
            :texts="['低', '中', '高']"
          />
        </el-form-item>
        
        <el-form-item label="解决状态">
          <el-switch v-model="issueDialog.form.resolved" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="issueDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleIssueSubmit">确认</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Back, Edit, Delete, Check, Close,
  Plus, Upload, Download, Document, SuccessFilled
} from '@element-plus/icons-vue'

const props = defineProps({
  project: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['back', 'update', 'delete'])

// 项目编辑功能
const isEditing = ref(false)
const form = reactive({
  name: '',
  description: ''
})

const handleEdit = () => {
  form.name = props.project.name
  form.description = props.project.description || ''
  isEditing.value = true
}

const saveEdit = () => {
  if (!form.name.trim()) {
    ElMessage.error('项目名称不能为空')
    return
  }
  
  const updatedProject = {
    ...props.project,
    ...form,
    updatedAt: new Date().toISOString()
  }
  emit('update', updatedProject)
  isEditing.value = false
  ElMessage.success('项目更新成功')
}

const cancelEdit = () => {
  isEditing.value = false
}

const confirmDelete = () => {
  ElMessageBox.confirm('确定删除该项目吗？', '警告', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    emit('delete', props.project.id)
    ElMessage.success('项目已删除')
  })
}

// 问题管理功能
const issueDialog = reactive({
  visible: false,
  mode: 'create',
  form: {
    description: '',
    ID: '',
    priority: 1,
    resolved: false
  }
})

const showIssueDialog = (mode, row) => {
  issueDialog.mode = mode
  if (mode === 'edit') {
    issueDialog.form = { 
      id: row.id,
      description: row.description,
      priority: row.priority,
      resolved: row.resolved,
      createdAt: row.createdAt
    }
  } else {
    issueDialog.form = {
      id: Date.now(), // 默认生成时间戳ID
      description: '',
      priority: 1,
      resolved: false,
      createdAt: new Date().toISOString()
    }
  }
  issueDialog.visible = true
}

const handleIssueSubmit = () => {
  const issueId = Number(issueDialog.form.id)
  if (isNaN(issueId)) {
    ElMessage.error('ID必须是有效数字')
    return
  }

  // 创建模式检查ID唯一性
  if (issueDialog.mode === 'create') {
    const exists = props.project.issues.some(i => i.id === issueId)
    if (exists) {
      ElMessage.error(`ID ${issueId} 已存在，请使用唯一标识`)
      return
    }
  }

  // 更新数据逻辑
  const updatedProject = { ...props.project }
  if (issueDialog.mode === 'create') {
    updatedProject.issues.push({
      ...issueDialog.form,
      id: issueId,  // 使用用户输入的ID
      createdAt: new Date().toISOString()
    })
  } else {
    const index = updatedProject.issues.findIndex(i => i.id === issueId)
    if (index > -1) {
      updatedProject.issues[index] = {
        ...updatedProject.issues[index],
        ...issueDialog.form,
        updatedAt: new Date().toISOString()
      }
    }
  }
  
  emit('update', updatedProject)
  issueDialog.visible = false
  ElMessage.success(`问题${issueDialog.mode === 'create' ? '添加' : '更新'}成功`)
}

const deleteIssue = (id) => {
  const updatedProject = {
    ...props.project,
    issues: props.project.issues.filter(i => i.id !== id)
  }
  emit('update', updatedProject)
  ElMessage.success('问题已删除')
}

// 文件管理功能
const handleUpload = (file) => {
  const newFile = {
    id: Date.now(),
    name: file.name,
    size: `${(file.size / 1024).toFixed(1)}KB`,
    type: file.type,
    raw: file,
    createdAt: new Date().toISOString()
  }

  const updatedProject = {
    ...props.project,
    files: [...props.project.files, newFile]
  }
  emit('update', updatedProject)
  return false
}

const deleteFile = (id) => {
  const updatedProject = {
    ...props.project,
    files: props.project.files.filter(f => f.id !== id)
  }
  emit('update', updatedProject)
  ElMessage.success('文件已删除')
}

const downloadFile = (file) => {
  if (file.raw) {
    const url = URL.createObjectURL(file.raw)
    const link = document.createElement('a')
    link.href = url
    link.download = file.name
    link.click()
    URL.revokeObjectURL(url)
  } else {
    ElMessage.warning('本地文件不可下载')
  }
}

// 工具函数
const formatTime = (time) => {
  return new Date(time).toLocaleString() // 确保传入的是有效时间戳或ISO字符串
}

const priorityType = computed(() => (priority) => {
  return {
    1: 'success',
    2: 'warning',
    3: 'danger'
  }[priority]
})
</script>

<style scoped>
.text-button {
  margin-left: auto;
  border-radius: 6px;
  padding: 8px 20px;
  background: linear-gradient(145deg, #409EFF, #79BBFF) !important;
  border-color: #409EFF !important;
  color: white !important;
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(64,158,255,0.2);
}

.text-button:hover {
  background: linear-gradient(145deg, #79BBFF, #409EFF) !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(64,158,255,0.3);
}

.text-button:active {
  transform: translateY(0);
}
.project-detail {
  margin: 20px;
  padding: 24px;
}

.header-actions {
  margin-bottom: 24px;
  display: flex;
  gap: 12px;
}

.project-info {
  margin-bottom: 32px;
  
  .project-name {
    margin: 0 0 12px 0;
    font-size: 24px;
  }
  
  .description {
    display: block;
    margin-bottom: 8px;
    color: #666;
  }
  
  .create-time {
    font-size: 12px;
    color: #999;
  }
}

.section-title {
  margin-right: 12px;
  font-size: 16px;
}

.issue-item, .file-item {
  display: flex;
  align-items: center;
  gap: 8px;
  
  .status-tag {
    display: inline-flex;
    align-items: center;
  }
}

.file-icon {
  margin-right: 8px;
  color: #666;
}

.form-actions {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.file-divider {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

/* 保持原有其他样式不变 */
.section-title {
  margin-right: 12px;
  font-size: 16px;
}
</style>
