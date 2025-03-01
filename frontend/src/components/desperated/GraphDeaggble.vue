<template>
  <div
    class="drag-container"
    ref="root"
  >
    <div class="header_view">
    <slot name="header">
    </slot>
    </div>
    <div
      v-for="(item, index) in filenames.filter(i=>i.show===true)"
      :key="item.name"
      class="draggable-item"
      :style="getItemStyle(item,index)"
      >



  <el-card style="width: 260px;height: 270px" >
    <template #header >
      <div style="cursor: move; padding: 0px">
         <el-row  class="space-between"  @mousedown.stop="startDragItem($event, index)">
           <el-col :span="16" ><el-text truncated>{{item.name}}</el-text></el-col>
           <el-col :span="4">  <el-button @click="clickItem(index)" circle :icon="Expand"></el-button></el-col>
            <el-col :span="4">  <el-button @click="hideElement(item)" circle :icon="Hide"></el-button></el-col>
        <el-col :span="2"> <el-space></el-space></el-col>
      </el-row>
      </div>
    </template>
<el-row>
    <div v-if="item.read" v-katex="renderMatrix(item.mat)" style="text-align: center;width: 100%;"> </div>
      <el-divider/>
        <el-text v-if="item.read"  type="info">维度: {{item.mat.length}}x{{item.mat[0].length}}</el-text>




</el-row>





  </el-card>

    </div>
    <!-- Button to add a new item -->
<!--    <el-button @click="addElement">Add Element</el-button>-->
  </div>
</template>

<script setup>
import {ref} from 'vue';

import {
Expand,Hide
} from '@element-plus/icons-vue'

const props=defineProps({
filenames:Array
})
const emits=defineEmits(['item_click'])
// export default {
//   props:{
//     data
//   },
  // computed: {
  //   Close() {
  //     return Close
  //   }
  // },
  // data() {
  //   return {
      const testelements=ref([
        { id: 1, text: '元素 1', top: 100, left: 100 },
        { id: 2, text: '元素 2', top: 200, left: 200 },
        { id: 3, text: '元素 3', top: 300, left: 300 }
      ]);
      const dragging=ref(false);
      const currentElementIndex=ref(-1);
      const offsetX=ref(0);
      const offsetY=ref(0);
      const containerOffsetX=ref(0);
      const containerOffsetY=ref(0);
      const isDraggingContainer=ref(false);
      const root= ref(null);


  //   };
  // },
  // methods: {


import katex from 'katex'


// Example matrix data



const matrixToLatex = (matrix) => {
  const maxRows = 4;
  const maxCols = 4;

  const rowCount = matrix.length;
  const colCount = matrix[0].length;
if(rowCount<=4&&colCount<=4)
{
  return arraytoMat(matrix)
}
  let truncatedMatrix = matrix.slice(0, 2); // Take first 2 rows

  if (rowCount > maxRows) {
    truncatedMatrix.push(new Array(colCount).fill('...')); // Add the ellipsis row
  }
  if(rowCount>4){
  truncatedMatrix = truncatedMatrix.concat(matrix.slice(rowCount - 1));
}
  else{
  truncatedMatrix = truncatedMatrix.concat(matrix.slice(2,rowCount));
  }
  truncatedMatrix = truncatedMatrix.map(row => {
    if (colCount > maxCols) {
      return row.slice(0, 2).concat(["..."]).concat(row.slice(colCount - 1));
    }
    return row;
  });
  return arraytoMat(truncatedMatrix)

}
const arraytoMat=(arr)=>
{
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

    const getItemStyle=(item,index)=> {
      if(!item.hasOwnProperty('top')){
            let num_row=Math.floor(index/3)
      let num_col=index%3
        item.top=50+num_row*280
        position: 'absolute'
        item.left=30+num_col*300
      }
               return {
        position: 'absolute',
        top: `${item.top}px`,
        left: `${item.left}px`,
      };
    };
    const getCursor=()=>
    {
      return{cursor: dragging.value ? 'grabbing' : 'grab'};
    };

    // Start dragging a specific item
    const startDragItem=(event, index)=> {
      dragging.value = true;
      currentElementIndex.value = index;
      const element = props.filenames[index];
      offsetX.value = event.clientX - element.left;
      offsetY.value = event.clientY - element.top;

      // Add global event listeners for mousemove and mouseup
      window.addEventListener('mousemove', dragMove);
      window.addEventListener('mouseup', endDrag);
      window.addEventListener('mouseleave', endDrag); // for mouse leaving the viewport
    };

    // Start dragging the container (empty space)
    const startDragContainer=(event)=> {
      isDraggingContainer.value = true;
      containerOffsetX.value = event.clientX - containerOffsetX;
      containerOffsetY.value = event.clientY - containerOffsetY;

      // Add global event listeners for mousemove and mouseup
      window.addEventListener('mousemove', dragMove);
      window.addEventListener('mouseup', endDrag);
      window.addEventListener('mouseleave', endDrag); // for mouse leaving the viewport
    };

    // During drag, update the element or container position
    const dragMove=(event)=> {
      if (dragging.value && currentElementIndex.value !== -1) {
        // Dragging an element
        const element = props.filenames[currentElementIndex.value];
        element.left = event.clientX - offsetX.value;
        element.top = event.clientY - offsetY.value;

        // Constrain the draggable item within the parent bounds
        // const parentRect = $el.getBoundingClientRect();
        const parentRect = root.value.getBoundingClientRect();
        const minX = 0;
        const minY = 0;
        const maxX = parentRect.width - 100; // item width
        const maxY = parentRect.height - 100; // item height

        element.left = Math.max(minX, Math.min(element.left, maxX));
        element.top = Math.max(minY, Math.min(element.top, maxY));
      } else if (isDraggingContainer.value) {
        // Dragging the entire container
        const container = root.value;
        const parentRect = container.getBoundingClientRect();
        containerOffsetX.value = event.clientX - containerOffsetX.value;
        containerOffsetY.value = event.clientY - containerOffsetY.value;

        const minX = 0;
        const minY = 0;
        const maxX = window.innerWidth - parentRect.width;
        const maxY = window.innerHeight - parentRect.height;

        containerOffsetX.value = Math.max(minX, Math.min(containerOffsetX.value, maxX));
        containerOffsetY.value = Math.max(minY, Math.min(containerOffsetY.value, maxY));

        container.style.left =containerOffsetX.value + 'px';
        container.style.top = containerOffsetY.value + 'px';
      }
    };

    // End the drag action
    const endDrag=()=> {
      if (dragging.value) {
        dragging.value= false;
        currentElementIndex.value = -1;
      }

      if (isDraggingContainer.value) {
        isDraggingContainer.value = false;
      }

      // Remove global event listeners after drag ends
      window.removeEventListener('mousemove', dragMove);
      window.removeEventListener('mouseup', endDrag);
      window.removeEventListener('mouseleave', endDrag);
    };

    // Method to add a new element
    const addElement=()=> {
      const newElement = {
        id: elements.value.length + 1, // Unique ID for the new element
        text: `元素 ${elements.value.length + 1}`,
        top: 50, // Default position
        left: 50
      };
      elements.value.push(newElement);
    };

    // Method to delete an element
    const hideElement=(item)=> {
      item.show=false;
    };

    const clickItem=(id)=>
    {
      const ell=props.filenames[id];
      emits("item_click",ell);
      console.log(dragging.value);
    };
  // }
// };
</script>

<style scoped>
.drag-container {
  position: relative;
  //width: 100%;
  min-width: 500px;
  min-height: 500px;
  height: 100%;
  border: 1px solid #ccc;
  background-color: #f0f0f0;
  overflow: hidden;

}

.draggable-item {
  //width: 100px;
  //height: 100px;
  //background-color: rgba(0, 150, 255, 0.7);
  //color: white;
  //text-align: center;
  //line-height: 100px;
  //border-radius: 8px;
  //position: absolute;
  //cursor: grab;
}

.draggable-item:active {
  //cursor: grabbing;
}
.header_view
{
  position: absolute;
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
