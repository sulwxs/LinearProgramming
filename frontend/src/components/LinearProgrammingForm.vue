<template>
  <el-button plain @click="dialogVisible = true">
    Open the fullscreen Dialog
  </el-button>
  <el-dialog
    v-model="dialogVisible"
    fullscreen
    top="40vh"
    width="70%"

  >
    <MatrixTable v-if="dialogVisible" :file="file_temp" ref="excel_editor"/>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="dialogVisible = false">
          确定
        </el-button>
      </div>
    </template>
  </el-dialog>
  <el-card class="overview">

    <template #header>
      <div class="card-header">
        <span>输入数据</span>
      </div>
    </template>
    <template #footer>
      <!--      <el-button type="success" @click="submitForm">计算</el-button>-->
    </template>
    <el-steps style="max-width: 600px" :active="step" finish-status="success">
      <el-step title="步骤 1" description="目标函数系数c" :status="matC?'success':'process'"/>
      <el-step title="步骤 2" description="约束条件矩阵A" :status="matA?'success':'process'"/>
      <el-step title="步骤 3" description="输入约束常数b" :status="matB?'success':'process'"/>
      <el-step title="步骤 4" description="求解" :status="result?'success':(errorMessage?'error':'process')"/>
    </el-steps>
    <el-divider></el-divider>
     <div> <p  class="text item">目标函数系数</p>
          <el-row>
            <el-col :span="1">
              <el-button @click="()=>{edithandle('c')}">编辑</el-button>
            </el-col>
            <el-col :span="22">
               <el-select placeholder="选择目标函数系数c" v-model="matC" value-key="name" @change="onchangeC">
              <el-option
                         key="matC"
                         label="c"
                         :value="input_c"/>


              <el-option v-for="f in fileLists"
                         :key="f.name"
                         :label="f.name"
                         :value="f"/>

            </el-select>
            </el-col>
  </el-row>
                 <el-row>
            <el-col :span="1">
              <el-button @click="()=>{edithandle('a')}">编辑</el-button>
            </el-col>
            <el-col :span="22">
              <el-select :span="12" placeholder="约束条件矩阵A" v-model="matA" value-key="name" @change="onchangeA">
                          <el-option
                         key="matA"
                         label="A"
                         :value="input_a"/>
              <el-option v-for="f in fileLists"
                         :key="f.name"
                         :label="f.name"
                         :value="f"/>
            </el-select>
            </el-col>
  </el-row>
                 <el-row>
            <el-col :span="1">
              <el-button @click="()=>{edithandle('b')}">编辑</el-button>
            </el-col>
            <el-col :span="22">

            <el-select :span="12" placeholder="输入约束常数b" v-model="matB" value-key="name" @change="onchangeB">
                          <el-option
                         key="matB"
                         label="b"
                         :value="input_b"/>
              <el-option v-for="f in fileLists"
                         :key="f.name"
                         :label="f.name"
                         :value="f"/>
            </el-select>
            </el-col>
  </el-row>



        </div>
        <el-button type="success" @click="submitMats" style="margin-top: 20px;">计算</el-button>


    <div style="height: 20px"></div>

    <div v-loading="solving">


      <div v-if="errorMessage" class="error">
        <el-text type="danger">错误: {{ errorMessage }}</el-text>
      </div>
      <div v-if="result">
        <el-text><h2>求解结果</h2></el-text>
        <el-divider></el-divider>
        <el-row>
          <el-col :span="3"><strong>最优解:</strong></el-col>
          <el-col :span="10">
            <el-text size="large">{{ toRaw(result.optimal_solution) }}</el-text>
<!--            <div v-if="result" v-katex="renderMatrix(toRaw(result.optimal_solution))" style="text-align: center;width: 100%;"></div>-->

          </el-col>
          <el-col :span="6">
            <el-button type="primary" @click="openresult" circle :icon="Expand"></el-button>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="3">
            <el-text size="large">最小值:</el-text>
          </el-col>
          <el-col :span="6">
            <el-text type="primary" size="large">
              <div/>
              {{ result.optimal_value }}
            </el-text>
          </el-col>

        </el-row>

      </div>
    </div>
  </el-card>


</template>

<script setup>
import {ref, defineEmits, defineProps} from 'vue'
import axios from "axios";
import {toRaw} from "vue";
import katex from 'katex'
import {Expand} from "@element-plus/icons-vue";
import MatrixTable from "@/components/MatrixTable.vue";
const excel_editor = ref(null)
const emits=defineEmits(['create_matrix'])
const props = defineProps({fileLists: Array})
// export default {
//   data() {
//     return {
const step = ref(0);
const solving = ref(false);
const numCoefficients = ref(3);
// const c = ref([]);
const numRows = ref(2);
const matrixA = ref(Array.from({length: 2}, () => Array(3).fill(0)));
const matrixB = ref(Array(2).fill(0));
const result = ref(null);
const errorMessage = ref(null);
const input_c=ref({read:true,show:true,mat:[],name:'矩阵c'})
const input_a=ref({read:true,show:true,mat:[],name:'矩阵A'})
const input_b=ref({read:true,show:true,mat:[],name:'矩阵b'})
const matC = ref(null)
const matA = ref(null)
const matB = ref(null)
const file_temp=ref(null)

const nextStep = () => {
  if (step.value >= 4)
    return;
  step.value++
}
const lastStep = () => {
  if (step.value <= 0)
    return;
  step.value--
}

const onchangeA=(i)=>
{
  console.log(i)
  step.value=Math.max(2,step.value)
  if(i.name==='矩阵A'){
    matA.value=input_a.value
    create_matrix_handle(matA)
  }
}
const onchangeB=(i)=>
{
  step.value=Math.max(3,step.value)
    if(i.name==='矩阵b'){
      matB.value=input_b.value
    create_matrix_handle(matB)
  }
}
const onchangeC=(i)=>

{
  console.log(i)
  step.value=Math.max(1,step.value)
    if(i.name==='矩阵c'){
      matC.value=input_c.value
    create_matrix_handle(matC)
  }
}
const create_matrix_handle=(mat)=>
{
  file_temp.value=mat.value
  // emits('create_matrix',mat)
  dialogVisible.value=true
}
const edithandle=(i)=>{
switch (i) {
  case 'a':file_temp.value=matA.value;break;
  case 'b':file_temp.value=matB.value;break;
  case 'c':file_temp.value=matC.value;break;

}


  dialogVisible.value=true
  console.log(file_temp.value)
  excel_editor.value.loadFile(file_temp.value)


}
const dialogVisible=ref(false)
const onNewfile=(mat)=>
{
  // console.log(mat)
  dialogVisible.value=true;
}
const generateCoefficients = () => {
  c.value = Array(numCoefficients.value).fill(0);
  matrixA.value = Array.from({length: numRows.value}, () => Array(numCoefficients.value).fill(0));
};
const goToStep = (step) => {
  if (step.value === 2) {
    if (numCoefficients.value <= 0 || c.value.includes('')) {
      alert('请填写目标函数系数');
      return;
    }
  } else if (step === 3) {
    if (numRows.value <= 0 || matrixA.value.flat().includes('')) {
      alert('请填写约束条件系数矩阵');
      return;
    }
  } else if (step === 1) {
    if (matrixB.value.includes('')) {
      alert('请填写约束常数');
      return;
    }
  }

  step.value = step;
};
const submitForm = async () => {
  solving.value = true
  try {
    const response = await axios.post("http://localhost:5000/solve", {
      c: c.value,
      A: matrixA.value,
      b: matrixB.value,
    });

    result.value = response.data;
    errorMessage.value = null;
    solving.value = false;
  } catch (error) {
    if (error.response) {
      errorMessage.value = error.response.data.message;
    } else {
      errorMessage.value = "请求失败，请检查输入";
    }
    result.value = null;
    solving.value = false;
  }
};
const submitMats = async () => {
  solving.value = true
  try {
    const response = await axios.post("http://localhost:5000/solve", {
      c: matC.value.mat,
      A: matA.value.mat,
      b: matB.value.mat,
    });

    result.value = response.data;
    errorMessage.value = null;
    solving.value = false;
  } catch (error) {
    if (error.response) {
      errorMessage.value = error.response.data.message;
    } else {
      errorMessage.value = "请求失败，请检查输入";
    }
    result.value = null;
    solving.value = false;
  }
};

const matrixToLatex = (matrix) => {
  const maxRows = 4;
  const maxCols = 4;

  const rowCount = matrix.length;
  const colCount = matrix[0].length;
  if (rowCount <= 4 && colCount <= 4) {
    return arraytoMat(matrix)
  }
  let truncatedMatrix = matrix.slice(0, 2); // Take first 2 rows

  if (rowCount > maxRows) {

    truncatedMatrix.push(new Array(colCount).fill('...')); // Add the ellipsis row
  }
  if (rowCount > 4) {
    truncatedMatrix = truncatedMatrix.concat(matrix.slice(rowCount - 1));
  } else {
    truncatedMatrix = truncatedMatrix.concat(matrix.slice(2, rowCount));
  }
  truncatedMatrix = truncatedMatrix.map(row => {
    if (colCount > maxCols) {
      return row.slice(0, 2).concat(["..."]).concat(row.slice(colCount - 1));
    }
    return row;
  });
  return arraytoMat(truncatedMatrix)

}
const arraytoMat = (arr) => {
  console.log(arr)
  let latexString = '\\begin{pmatrix}';
  arr.forEach(row => {

    latexString += row.join(' & ') + '\\\\';


  });
  latexString += '\\end{pmatrix}';

  return latexString;
}
const renderMatrix = (matrix) => {
  console.log(matrix)
  const latexFormula = matrixToLatex(matrix);
  return latexFormula;
}
const openresult=()=>
{

  const refile={name:'结果',mat:[toRaw(result.value.optimal_solution)]}
  file_temp.value=refile
  dialogVisible.value=true
  console.log(file_temp)
  excel_editor.value.loadFile(refile)
}
</script>

<style scoped>
.overview {
  margin-top: 36px;
  height: calc(100vh - 120px);
}
</style>
