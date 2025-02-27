<template>
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

          <GraphList style="height:80vh" :filenames="fileLists" @item_click="openTab">
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
          </GraphList>

        </el-tab-pane>
        <el-tab-pane
            v-for="item in editableTabs"
            :key="item.name"
            :label="item.name"
            :name="item.name">
            <ExcelTable :matData="props.fileLists.find(i=>i.name===item.name).mat"></ExcelTable>

        </el-tab-pane>
      </el-tabs>


</template>

<script setup>
import {ref,defineEmits,defineProps} from 'vue';
import upload from "@/components/upload.vue";
import MatrixTable from "@/components/MatrixTable.vue";
// import GraphDeaggble from "@/components/GraphDeaggble.vue";
import GraphList from "@/components/GraphList.vue";
import {Select} from '@element-plus/icons-vue';
import axios from "axios";
import {ElMessage} from "element-plus";
import ExcelTable from "@/components/ExcelTable.vue";

const props=defineProps({fileLists:Array});
const  emits=defineEmits(['filelistchange'])
// const props=defineProps({fileLists:Array,})
const name = ref('app');
const show_selected_table = ref(false);
// const show_file_list = ref([])
// const dataa = ref([]);
const editableTabsValue = ref('overview');
// const fileLists = ref([]);
const loading = ref(false);
const editableTabs = ref([]);
const handleChange = async () => {
  for(let item of fileLists)
{
        if(!item.read){
          await readFile(item.name)
           emits('filelistchange',fileLists)
        }
      }

};

const readFile = async (filename) => {
  loading.value = true;
  try {
    const response = await axios.get(`http://127.0.0.1:5000/read_csv_matrix?filename=${filename}`);
    if (response.data.matrix) {
      var a = props.fileLists.find(item => item.name === filename);
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
  // editableTabsValue.value = activeName
  editableTabsValue.value = 'overview'
  props.fileLists.find(i=>i.name===currentTab).hasopen=false
  editableTabs.value = tabs.filter((tab) => tab.name !== currentTab)
};

</script>
<style scoped>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;

}
.demo-tabs{
  width: 100%;
  height: 100%;
}
</style>
