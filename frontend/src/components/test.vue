<template>
  <div class="app">
<!--    <h1>线性规划求解器</h1>-->


    <div class="container">
      <div class="overview">
        <h3>输入数据总览</h3>
        <p><strong>目标函数系数:</strong> {{ c }}</p>
        <p><strong>约束条件矩阵A:</strong></p>
        <table v-if="numRows > 0 && numCoefficients > 0">
          <thead>
            <tr>
              <th v-for="colIndex in numCoefficients" :key="'col-' + colIndex">x{{ colIndex }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, rowIndex) in numRows" :key="'row-' + rowIndex">
              <td v-for="colIndex in numCoefficients" :key="'input-' + rowIndex + '-' + colIndex">
                {{ matrixA[rowIndex][colIndex - 1] }}
              </td>
            </tr>
          </tbody>
        </table>
        <p><strong>约束常数b:</strong> {{ matrixB }}</p>
        <button>求解</button>
      </div>
      <div class="steps-container">

        <div class="step-bar">
          <div
            class="step"
            :class="{ active: step >= 1 }"
          >步骤 1: 选择目标函数系数个数</div>
          <div
            class="step"
            :class="{ active: step >= 2 }"
          >步骤 2: 输入约束条件矩阵A</div>
          <div
            class="step"
            :class="{ active: step >= 3 }"
          >步骤 3: 输入约束常数b</div>
        </div>

        <!-- 步骤1-->
        <div v-show="step === 1" class="form-group">
          <label for="numCoefficients">目标函数系数个数：</label>
          <input
            type="number"
            v-model="numCoefficients"
            min="1"
            placeholder="输入目标函数系数的个数"
            @input="generateCoefficients"
            :class="{'invalid-input': numCoefficients <= 0}"
          />

          <div v-if="numCoefficients > 0">
            <label v-for="(index) in numCoefficients" :key="'c' + index">
              c{{ index }}:
              <input
                type="number"
                v-model="c[index - 1]"
                :placeholder="'输入c' + index"
                :class="{'invalid-input': !c[index - 1]}"
              />
            </label>
          </div>

          <button
            @click="goToStep(2)"
            :disabled="numCoefficients <= 0 || c.includes('')"
          >
            下一步
          </button>
        </div>

        <!-- 步骤2-->
        <div v-show="step === 2" class="form-group">
          <label for="A">约束条件系数矩阵 (A):</label>
          <div>
            <label>约束条件的行数：</label>
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
                    <input
                      type="number"
                      v-model="matrixA[rowIndex][colIndex - 1]"
                      :placeholder="'a' + (rowIndex + 1) + (colIndex)"
                      :class="{'invalid-input': matrixA[rowIndex][colIndex - 1] === ''}"
                    />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>  <button @click="goToStep(1)">上一步</button>
          <button @click="goToStep(3)" :disabled="numRows <= 0 || matrixA.flat().includes('')">下一步</button>

        </div>

        <!-- 步骤3-->
        <div v-show="step === 3" class="form-group">
          <label for="b">约束常数 (b):</label>
          <div>
            <div v-for="(val, index) in numRows" :key="'b-' + index">
              <input
                type="number"
                v-model="matrixB[index]"
                :placeholder="'b' + (index + 1)"
                :class="{'invalid-input': matrixB[index] === ''}"
              />
            </div>
          </div>   <button @click="goToStep(2)">上一步</button>
          <button @click="submitForm" :disabled="matrixB.includes('')">提交求解</button>

        </div>

        <div v-if="result" class="result">
          <h2>求解结果</h2>
          <p><strong>最优解:</strong> {{ result.optimal_solution }}</p>
          <p><strong>最小值:</strong> {{ result.optimal_value }}</p>
        </div>

        <div v-if="errorMessage" class="error">
          <p><strong>错误:</strong> {{ errorMessage }}</p>
        </div>
      </div>


    </div>
  </div>
</template>

<script setup>
import axios from "axios";

// export default {
//   data() {
//     return {
      const step=ref(1);
      const numCoefficients=ref(3);
      const c=ref([]);
      const numRows=ref(2);
      const matrixA=ref(Array.from({ length: 2 }, () => Array(3).fill(0)));
      const matrixB=ref(Array(2).fill(0));
      const result=ref(null);
      const errorMessage=ref(null);
  //   };
  // },
  // methods: {

    const generateCoefficients=() =>{
      this.c = Array(this.numCoefficients).fill(0);
      this.matrixA = Array.from({ length: this.numRows }, () => Array(this.numCoefficients).fill(0));
    };
    const goToStep=(step) =>{
      if (step === 2) {
        if (this.numCoefficients <= 0 || this.c.includes('')) {
          alert('请填写目标函数系数');
          return;
        }
      } else if (step === 3) {
        if (this.numRows <= 0 || this.matrixA.flat().includes('')) {
          alert('请填写约束条件系数矩阵');
          return;
        }
      } else if (step === 1) {
        if (this.matrixB.includes('')) {
          alert('请填写约束常数');
          return;
        }
      }

      this.step = step;
    };
    const submitForm=async ()=> {
      try {
        const response = await axios.post("http://localhost:5000/solve", {
          c: this.c,
          A: this.matrixA,
          b: this.matrixB,
        });

        this.result = response.data;
        this.errorMessage = null;
      } catch (error) {
        if (error.response) {
          this.errorMessage = error.response.data.message;
        } else {
          this.errorMessage = "请求失败，请检查输入";
        }
        this.result = null;
      }
    };
  // },
// };
</script>

<style scoped>
.app {
  width: 100%;
  margin: 0 auto;
  padding-top: 20px;
  text-align: center;
}

.container {
  display: flex;
  justify-content: space-between;
}

.steps-container {
  flex: 3;
  margin-right: 20px;
}

.step-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.step {
  padding: 10px;
  width: 30%;
  text-align: center;
  background-color: #ddd;
  border-radius: 4px;
}

.step.active {
  background-color: #28a745;
  color: white;
}

.form-group {
  margin-bottom: 15px;
}

input,
textarea {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
}

table {
  margin: 20px auto;
  border-collapse: collapse;
}

table, th, td {
  border: 1px solid #ddd;
}

th, td {
  padding: 10px;
  text-align: center;
}

button {
  padding: 10px 15px;
  background-color: #28a745;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background-color: #218838;
}

.invalid-input {
  border: 2px solid red;
}

.overview {
  flex: 2;
  position: sticky;
  top: 20px;
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 300px;
  text-align: left;
  height: fit-content;
  overflow-y: auto;
}

.result {
  margin-top: 30px;
  padding: 15px;
  border: 1px solid #28a745;
  background-color: #d4edda;
}

.error {
  margin-top: 30px;
  padding: 15px;
  border: 1px solid #dc3545;
  background-color: #f8d7da;
}
</style>
