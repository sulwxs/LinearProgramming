<template>
  <div
      ref="root"
      class="drag-container"
  >
    <div class="header_view">
      <slot name="header">

      </slot>
    </div>
    <el-space class="graph" wrap>
      <div
          v-for="(item, index) in filenames.filter(i=>i.show===true)"
          :key="item.name"
      >
        <el-card style="width: 260px;height: 270px">
          <template #header>
            <div style="cursor: move; padding: 0px">
              <el-row class="space-between">
                <el-col :span="16">
                  <el-text truncated>{{ item.name }}</el-text>
                </el-col>
                <el-col :span="4">
                  <el-button :icon="Expand" circle @click="clickItem(index)"></el-button>
                </el-col>
                <el-col :span="4">
                  <el-button :icon="Hide" circle @click="hideElement(item)"></el-button>
                </el-col>
                <el-col :span="2">
                  <el-space></el-space>
                </el-col>
              </el-row>
            </div>
          </template>
          <el-row>
            <div v-if="item.read" v-katex="renderMatrix(item.mat)" style="text-align: center;width: 100%;"></div>
            <el-divider/>
            <el-text v-if="item.read" type="info">维度: {{ item.mat.length }}x{{ item.mat[0].length }}</el-text>


          </el-row>


        </el-card>

      </div>
    </el-space>

  </div>
</template>

<script setup>
import {ref} from 'vue';

import {
  Expand, Hide
} from '@element-plus/icons-vue'

const props = defineProps({
  filenames: Array
})
const emits = defineEmits(['item_click'])

const testelements = ref([
  {id: 1, text: '元素 1', top: 100, left: 100},
  {id: 2, text: '元素 2', top: 200, left: 200},
  {id: 3, text: '元素 3', top: 300, left: 300}
]);
const dragging = ref(false);
const currentElementIndex = ref(-1);
const offsetX = ref(0);
const offsetY = ref(0);
const containerOffsetX = ref(0);
const containerOffsetY = ref(0);
const isDraggingContainer = ref(false);
const root = ref(null);


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
  let latexString = '\\begin{pmatrix}';
  arr.forEach(row => {
    latexString += row.join(' & ') + '\\\\';
  });
  latexString += '\\end{pmatrix}';

  return latexString;
}
const renderMatrix = (matrix) => {
  const latexFormula = matrixToLatex(matrix);
  return latexFormula;
}


const hideElement = (item) => {
  item.show = false;
};

const clickItem = (id) => {
  const ell = props.filenames[id];
  emits("item_click", ell);
  console.log(dragging.value);
};

</script>

<style scoped>
.drag-container {
  //position: relative;
  //width: 100%;
  //min-width: 500px;
  //min-height: 500px;
  min-height: 40vmax;
  border: 1px solid #ccc;
  background-color: #f0f0f0;
  overflow: hidden;
  margin-right: 10px;
  padding-bottom: 10px;
}
@media screen and (max-width: 576px) {
   .graph {


     justify-content: center;
  }
}
.graph{
    padding-left: 10px;

  width: 100%;


}

.header_view {

  top: 0px;
  left: 0px;
  width: 100%;
  height: 40px;
  background-color: rgba(255, 255, 255, 0.7);
  z-index: 10;
}

* {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
</style>
