<template>


  <el-card class="overview">

    <template #header>
      <div class="card-header">
        <span>输入数据总览</span>
      </div>
    </template>

    <el-col>
      <p :span="12" class="text item">目标函数系数</p>
      <el-select :span="12" v-model="c">
        <el-option v-for="f in fileLists"
                   :key="f.name"
        :label="f.name"
        :value="f.mat"/>
      </el-select>
    </el-col>
      <el-select :span="12" v-model="matrixA">
        <el-option v-for="f in fileLists"
                   :key="f.name"
        :label="f.name"
        :value="f.mat"/>
      </el-select>
          <el-select :span="12" v-model="matrixB">
        <el-option v-for="f in fileLists"
                   :key="f.name"
        :label="f.name"
        :value="f.mat"/>
      </el-select>
    <template #footer>
      <el-button type="success" @click="submitForm">计算</el-button>
    </template>

    <div style="height: 20px"></div>
    <el-steps style="max-width: 600px" :active="step" finish-status="success">
      <el-step title="步骤 1" description="选择目标函数系数个数"/>
      <el-step title="步骤 2" description="输入约束条件矩阵A"/>
      <el-step title="步骤 3" description="输入约束常数b"/>
      <el-step title="步骤 4" description="求解"/>
    </el-steps>
    <el-form>      <!-- 步骤1-->
      <el-form-item v-show="step === 0" class="form-group">
        <el-text for="numCoefficients">目标函数系数个数：</el-text>
        <el-input
            type="number"
            v-model="numCoefficients"
            min="1"
            placeholder="输入目标函数系数的个数"
            @input="generateCoefficients"
        />

        <div v-if="numCoefficients > 0">

<el-col>
       <el-input
                v-for="(index) in numCoefficients" :key="'c' + index"
                :span="8"
                style="width: 100px;"
                type="number"
                v-model="c[index - 1]"
                :placeholder="'输入c' + index"
            />
</el-col>


        </div>

      </el-form-item>

      <!-- 步骤2-->
      <el-form-item v-show="step === 1" class="form-group">
        <div>
          <el-text>约束条件的行数：</el-text>
          <input
              type="number"
              v-model="numRows"
              min="1"
              placeholder="输入行数"
              :class="{'invalid-input': numRows <= 0}"
          />
        </div>
        <div v-if="numRows > 0">
          <table>
            <thead>
            <tr>
              <th v-for="colIndex in numCoefficients" :key="'col-' + colIndex">x{{ colIndex }}</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(row, rowIndex) in numRows" :key="'row-' + rowIndex">
              <td v-for="colIndex in numCoefficients" :key="'input-' + rowIndex + '-' + colIndex">
                <el-input
                    type="number"
                    v-model="matrixA[rowIndex][colIndex - 1]"
                    :placeholder="'a' + (rowIndex + 1) + (colIndex)"
                    style="width: 100px;"
                />
              </td>
            </tr>
            </tbody>
          </table>
        </div>


      </el-form-item>

      <!-- 步骤3-->
      <el-form-item v-show="step === 2" class="form-group">
        <div>
          <div v-for="(val, index) in numRows" :key="'b-' + index">
            <el-input
                type="number"
                v-model="matrixB[index]"
                :placeholder="'b' + (index + 1)"
                :class="{'invalid-input': matrixB[index] === ''}"
                style="width: 100px;"
            />
          </div>
        </div>


      </el-form-item>

      <el-form-item v-show="step === 3" class="result">
        <h2>求解结果</h2>
<!--        <p><strong>最优解:</strong> {{ result.optimal_solution }}</p>-->
<!--        <p><strong>最小值:</strong> {{ result.optimal_value }}</p>-->
      </el-form-item>
      <el-button v-if="step!==0&&step<4" style="margin-top: 12px" @click="lastStep" :disabled="solving">上一步</el-button>
      <el-button v-if="step<3" style="margin-top: 12px" @click="nextStep">下一步</el-button>


    </el-form>

    <div class="steps-container">


      <div v-if="errorMessage" class="error">
        <el-text type="danger">错误:{{ errorMessage }}</el-text>
      </div>
    </div>
<!--<div v-if="step===3" v-loading="solving">-->
<!--          <h2>求解结果</h2>-->
<!--        <p><strong>最优解:</strong> {{ result.optimal_solution }}</p>-->
<!--        <p><strong>最小值:</strong> {{ result.optimal_value }}</p>-->
<!--</div>-->
  </el-card>


</template>

<script setup>
import {ref, defineEmits, defineProps} from 'vue'
import axios from "axios";

const props = defineProps({fileLists: Array})
// export default {
//   data() {
//     return {
const step = ref(0);
const solving = ref(false);
const numCoefficients = ref(3);
const c = ref([]);
const numRows = ref(2);
const matrixA = ref(Array.from({length: 2}, () => Array(3).fill(0)));
const matrixB = ref(Array(2).fill(0));
const result = ref(null);
const errorMessage = ref(null);


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
//   };
// },
// methods: {

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
  solving.value=true
  try {
    const response = await axios.post("http://localhost:5000/solve", {
      c: c.value,
      A: matrixA.value,
      b: matrixB.value,
    });

    result.value = response.data;
    errorMessage.value = null;
    solving.value=false;
  } catch (error) {
    if (error.response) {
      errorMessage.value = error.response.data.message;
    } else {
      errorMessage.value = "请求失败，请检查输入";
    }
    result.value= null;
    solving.value=false;
  }
};
// },
// };
</script>

<style scoped>
.overview {
  margin-top: 22px;
}
</style>
