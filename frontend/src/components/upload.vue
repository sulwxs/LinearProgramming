<template>
  <div>
    <el-row >
      <!-- 文件上传区域 -->
    <el-upload
      class="upload-demo"
      action="http://127.0.0.1:5000/upload"
      :on-success="handleUploadSuccess"
      :on-progress="handleProgress"
      :before-upload="beforeUpload"
      multiple
      :show-file-list="false"
    >
<!--      :file-list="fileList"-->
      <el-button type="primary">选择文件</el-button>

    </el-upload>
      <div style="width: 10px"></div>
              <el-button
      type="primary"
      @click="downloadTemplate"
      style="margin-bottom: 20px"
    >
      <el-icon><Download /></el-icon>
      下载CSV模板
    </el-button>


    </el-row>


    <!-- 文件状态展示 -->
    <div v-if="fileList.length >=0" class="file-status-container">
      <el-table v-loading="loading"  :data="fileList" style="width: 100%">
        <el-table-column prop="name" label="文件名" align="center">
          <template #default="{ row }">
            <div @dblclick="row.edit=!row.edit">
                          <span v-show="!row.edit">{{row.alias}}</span>
          <el-input
             :autofocus="true"
            v-show="row.edit"
            v-model="row.alias"
            @focusout="row.edit=false"
            style="max-width: 250px"
          ></el-input>
            </div>


          </template>
        </el-table-column>
        <el-table-column prop="status" label="上传状态" align="center">
          <template #default="{ row }">
            <el-progress
              v-if="row.status === 'uploading'"
              :percentage="row.progress"
              status="active"
            />
              <el-icon v-else :style="row.status === 'success' ? { color: 'green' } : { color: 'red' }">
                <template v-if="row.status === 'success'">
                  <CircleCheckFilled />
                </template>
                <template v-else>
                  <CloseCircleFilled />
                </template>
              </el-icon>

          </template>
        </el-table-column>
        <el-table-column label="操作"  align="center">
          <template #default="{ row }">
<!--            <el-button-->
<!--              @click="deleteFile(row.name)"-->
<!--              size="small"-->
<!--              type="danger"-->
<!--            >-->
<!--              删除-->
<!--            </el-button>-->
  <el-dropdown @command="(e)=>handleFileAct(e,row)">
    <span class="el-dropdown-link">
      操作
      <el-icon class="el-icon--right">
        <ArrowDown/>
      </el-icon>
    </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item command="重命名">重命名</el-dropdown-item>
        <el-dropdown-item command="复制">复制</el-dropdown-item>
        <el-dropdown-item command="下载">下载</el-dropdown-item>
        <el-dropdown-item command="删除">删除</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>





          </template>
        </el-table-column>
      </el-table>
    </div>

<!--    &lt;!&ndash; 上传进度总览 &ndash;&gt;-->
<!--    <el-descriptions title="文件上传进度">-->
<!--      <el-descriptions-item label="上传进度">-->
<!--        <el-progress-->
<!--          :percentage="overallProgress"-->
<!--          status="active"-->
<!--        />-->
<!--      </el-descriptions-item>-->
<!--    </el-descriptions>-->
  </div>
</template>

<script setup>

import { ref ,defineEmits,defineProps} from 'vue';
import axios from 'axios';
import {
  ElUpload,
  ElButton,
  ElTable,
  ElTableColumn,
  ElProgress,
  ElDescriptions,
  ElDescriptionsItem,
  ElMessage,
  ElMessageBox
} from 'element-plus';
import {CircleCheckFilled, Rank, CircleCloseFilled, ArrowDown} from '@element-plus/icons-vue';

// export default {
  // emits:['loadfilenames'],
  // components: {
  //   CircleCheckFilled,
  //   ElUpload,
  //   ElButton,
  //   ElTable,
  //   ElTableColumn,
  //   ElProgress,
  //   ElDescriptions,
  //   ElDescriptionsItem,
  //   ElMessage,
  // },
  // setup() {

    const fileList = ref([]);
    const loading=ref(true);
    const overallProgress = ref(0);
    const emits = defineEmits(['loadfilenames','fileupload','filedelete']);




    // 文件上传成功后回调
    const handleUploadSuccess = (response, file) => {
      console.log(file)
      if(file.percentage==100){
      console.log(fileList.value)
      fileList.value.find(i=>i.name==file.name).status='success'
      ElMessage.success(`文件 "${file.name}" 上传成功`);
      emits('fileupload',file)
      // updateOverallProgress();
      }
      else
      {

      }

    };

    // 文件上传进度回调
    const handleProgress = (event, file, list) => {
      console.log(event.percent)
      const targetFile = fileList.value.find(f => f.name === file.name);
      if (targetFile) {
        targetFile.status = 'uploading';
        targetFile.progress = Math.round((event.percent || 0)); // 上传进度
      }
      // updateOverallProgress();
    };

    // 更新总进度
    const updateOverallProgress = () => {
      const totalProgress = fileList.value.reduce((acc, file) => acc + file.progress, 0);
      overallProgress.value = Math.round(totalProgress / fileList.value.length);
    };

    // 文件上传前的验证
    const beforeUpload = (file) => {
      const isAllowedType = ['text/plain', 'text/csv', 'application/octet-stream'].includes(file.type);
      if (!isAllowedType) {
        ElMessage.error('只能上传 .txt, .csv 或 .mat 文件');
      }
      let f=fileList.value.find(i=>i.name===file.name)
      if(f===undefined)
      {  const newFile = {
        name: file.name,
        status: 'uploading',
        progress: 0,
      };
      fileList.value.push(newFile);}
      else {
              f.status= 'uploading'
        f.progress= 0
        f.read=false
      }
      return isAllowedType;
    };
   const handleFileAct =(e,file)=>{
     const name=file.name
     console.log(file)
  switch (e){
   case '删除':
    deleteFile(file)
     break
    case '复制':
    copyFile(file)
     break
    case '重命名':
    renameFile(file,name)
     break
        case '下载':
        downloadFile(file)
     break
  }
}

    // 删除文件
    const deleteFile = async (file) => {
               ElMessageBox.confirm(
    '确定要删除文件 '+file.alias+' ?',
    'Warning',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/delete?filename=${file.name}`);
        if (response.data.success) {
          fileList.value = fileList.value.filter((f) => f.name !== file.name);
          emits('filedelete', file.name)
          ElMessage.success(`文件 "${file.alias}" 删除成功`);
        } else {
          ElMessage.error('删除失败');
        }
      } catch (error) {
        console.error('删除文件时发生错误', error);
        ElMessage.error('删除失败');
      }
    })
    .catch(() => {
      return
    })


    };
const renameFile = async (file,alias) => {


  ElMessageBox.prompt('输入文件名', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    inputPattern:
        /^[\u4e00-\u9fa5\w\s.-]+$/,
    inputErrorMessage: '无效文件名',
  })
      .then(async ({value}) => {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/rename?filename=${file.name}&alias=${value}`);
          if (response.data.success) {
            file.alias = alias
            emits('rename', file.alias)
            ElMessage.success(`文件 "${file.alias}" 重命名成功`);
          } else {
            ElMessage.error('重命名失败');
          }
        } catch (error) {
          console.error('发生错误', error);
          ElMessage.error('重命名失败');
        }

      })
      .catch(() => {

      })
};




const copyFile = async (file) => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/copy?filename=${file.name}`);
        if (response.data.success) {
          const new_f=response.data.file
          fileList.value.push(new_f);

          emits('copyfile',file.name)
          ElMessage.success(`文件 "${file.name}" 复制成功`);
        } else {
          ElMessage.error('复制失败');
        }
      } catch (error) {
        console.error('发生错误', error);
        ElMessage.error('复制失败');
      }
    };
const downloadFile = async (file) => {
      try {

        const response = await axios.get(`http://127.0.0.1:5000/download?filename=${file.name}`);
        console.log(file)
         const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', file.alias?file.alias:file.name);
        document.body.appendChild(link);
        link.click();

        // if (response.data.success) {
        //   fileList.value = fileList.value.filter((file) => file.name !== filename);
        //   emits('download',filename)
        //   ElMessage.success(`文件 "${filename}" 开始下载`);
        // } else {
        //   ElMessage.error('无法下载');
        // }
      } catch (error) {
        console.error('发生错误', error);
        ElMessage.error('无法下载');
      }
    };


        // 加载已有文件列表
    const loadFileList = async () => {
      try {
        loading.value=true;
        const response = await axios.get('http://127.0.0.1:5000/getfilelist');
        // console.error(['加载文件列', response.data]);
        if (response.data && Array.isArray(response.data)) {
          // for(file in response.data)
          // {//  { "name": "file1.txt", "status": "成功", "progress": 100 },
          //   fileList.value.join({name:file, "status": "成功", "progress": 100})
          // }
          // console.error('加载文件列失败', fileList);
          fileList.value = response.data; // 更新 fileList
          emits('loadfilenames',fileList.value)

        }
      } catch (error) {
        console.error('加载文件列表失败', error);
        ElMessage.error('加载文件列表失败');
        loading.value=false;
      }
      loading.value=false;
    };
    const downloadTemplate = () => {
      const csvContent = "1,2,3\n4,5,6\n7,8,9";
      const blob = new Blob([csvContent], { type: 'text/csv' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'template.csv';
      link.click();
      URL.revokeObjectURL(link.href);
      ElMessage.success('模板下载成功');
    };
    // 在组件挂载后加载文件列表
    // onMounted(() => {
    //
    // });

    loadFileList()

    // return {
    //   fileList,
    //   loading,
    //   overallProgress,
    //   handleUploadSuccess,
    //   handleProgress,
    //   beforeUpload,
    //   deleteFile,
    //   loadFileList,
    // };
  // },
// };
</script>

<style scoped>
.file-status-container {
  margin-top: 20px;
}

/* 表格头部居中 */
.el-table__header-wrapper {
  text-align: center;
}

/* 进度条样式 */
.el-progress {
  margin: 5px 0;
}
</style>
