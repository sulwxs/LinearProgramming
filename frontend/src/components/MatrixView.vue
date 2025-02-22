<template>
  <el-tabs tab-position="left" class="demo-tabs">
    <el-tab-pane label="矩阵选择">
      <el-tabs
          v-model="editableTabsValue"
          type="card"
          class="demo-tabs"
          closable
          @tab-remove="removeTab">
        <template #add-icon>
          <el-icon><Select/></el-icon>
        </template>
        <el-tab-pane key="overview"
                     label="全部矩阵"
                     name="overview">

          <GraphDeaggble :filenames="fileLists" @item_click="openTab">
            <template #header>
              <el-row style="height: 100%;padding: 0 8px 0 8px;" type="flex" justify="start" align="middle">
                <el-popover :visible="show_selected_table" placement="bottom" :width="320">
                  <p>选择要显示的数据</p>
                  <el-form-item @change="handleChange">

                    <el-checkbox v-for="file in fileLists" v-model="file.show" name="type">
                      {{ file.name }}
                    </el-checkbox>

                  </el-form-item>
                  <div style="text-align: right; margin: 0">
                    <!--                    <el-button size="small" text @click="show_selected_table = false">取消</el-button>-->
                    <el-button size="small" type="primary" @click="show_selected_table = false">
                      确定
                    </el-button>
                  </div>
                  <template #reference>
                    <el-button @click="show_selected_table = true" style="">显示</el-button>
                  </template>
                </el-popover>
              </el-row>
            </template>
          </GraphDeaggble>

        </el-tab-pane>
        <el-tab-pane
            v-for="item in editableTabs"
            :key="item.name"
            :label="item.name"
            :name="item.name"
        >
          {{ item.show }}
        </el-tab-pane>
      </el-tabs>
    </el-tab-pane>
    <el-tab-pane label="文件导入">
      <upload ref="upload_ref" @loadfilenames="loadFileNames" @filedelete="handleDeleteFile" @fileupload="handleFileUpload"></upload>
    </el-tab-pane>

  </el-tabs>

</template>

<script setup>
import {ref} from 'vue';
import upload from "@/components/upload.vue";
import ExcelTable from "@/components/ExcelTable.vue";
import GraphDeaggble from "@/components/GraphDeaggble.vue";
import {Select} from '@element-plus/icons-vue';
import axios from "axios";
import {ElMessage} from "element-plus";
// import type { TabPaneName } from 'element-plus';
// export default {
//   components: {ExcelTable, upload, GraphDeaggble},
//   setup() {
const name = ref('app');
const show_selected_table = ref(false);
const show_file_list = ref([])
const dataa = ref([]);
const editableTabsValue = ref('overview');
const fileLists = ref([]);
const loading = ref(false);
const editableTabs = ref([]);
const handleChange = async () => {
  for(let item of fileLists.value)
{
        if(!item.read){
          await readFile(item.name)
        }
      }

};
const loadallMatx = async () => {
  loading.value = true;
  try {

    for (let file of fileLists.value) {
      if (file.read === false) {
        await readFile(file.name);
      }
    }
  } catch (error) {
    console.log(error)
  }
  loading.value = false;
};
const readFile = async (filename) => {
  loading.value = true;
  try {
    const response = await axios.get(`http://127.0.0.1:5000/read_csv_matrix?filename=${filename}`);
    if (response.data.matrix) {
      var a = fileLists.value.find(item => item.name === filename);
      a.mat = response.data.matrix;
      a.read = true;
    } else {
      ElMessage.error('读取失败');
      a.read=false;
    }
  } catch (error) {
    console.error('读取文件时发生错误', error);
    ElMessage.error('读取失败');
      a.read=false;

  }
  loading.value = false;
};
const loadFileNames = (files) => {
  fileLists.value = files;

  loadallMatx();
};
const handleDeleteFile=(filename)=>
{
  fileLists.value=fileLists.value.filter(f=>f.name!==filename)
}
const handleFileUpload=(file)=>
{
  const nf={name:file.name,status:"success",progress:100,read:false,show:false,open:false}
fileLists.value.push(nf)
  console.log(fileLists)
}
const openTab=(file)=>
{
  if(file.hasOwnProperty('hasopen')&&file.hasopen){



  }
  else {
    file.hasopen=true
  let a={name:file.name}
  editableTabs.value.push(a)
  }
 editableTabsValue.value = file.name
};
const removeTab = (currentTab) => {
  console.log(currentTab)
  const tabs = editableTabs.value
  let activeName = editableTabsValue.value
  if (activeName === currentTab) {
    tabs.forEach((tab, index) => {
      if (tab.name === currentTab) {
        const nextTab = tabs[index + 1] || tabs[index - 1]
        if (nextTab) {
          activeName = nextTab.name
        }
      }
    })
  }
  editableTabsValue.value = activeName
  fileLists.value.find(i=>i.name===currentTab).hasopen=false
  editableTabs.value = tabs.filter((tab) => tab.name !== currentTab)
};
//   return {name, show_selected_table,show_file_list, filenames,dataa, editableTabs, editableTabsValue, loadFileNames,removeTab};
// },

// };

</script>
<style scoped>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
</style>
