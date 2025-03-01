<template>

  <div ref="container" class="excel_container" :id="'container'+props.file.name"></div>
</template>

<script setup>
import {onMounted, onBeforeUnmount,reactive, toRaw,defineExpose} from 'vue'

import {createUniver, defaultTheme, LocaleType, merge, UniverInstanceType} from '@univerjs/presets';
import {UniverSheetsCorePreset} from '@univerjs/presets/preset-sheets-core';
import UniverPresetSheetsCoreZhCN from '@univerjs/presets/preset-sheets-core/locales/zh-CN';
import {Univer} from "@univerjs/presets";
import '@univerjs/presets/lib/styles/preset-sheets-core.css';
import {Worksheet} from "@univerjs/presets";


const csvtoWorkBook=(file)=>{
  const cellData = {};
  // 遍历二维数组的每一行
  file.mat.forEach((row, rowIndex) => {
    // 遍历每一行的每一列

    cellData[rowIndex] = {};
    row.forEach((cellValue, colIndex) => {
      // 将二维数组的值赋给 IWorksheetData 格式
      cellData[rowIndex][colIndex] = { v: cellValue };
    });
  });

  return  cellData ;
}
const workBooktoCSV=(data)=>{
  // 获取所有行的数据
  const rows = Object.keys(data.cellData);
  // 遍历每一行，并提取每一列的数据
  const result = rows.map(rowIndex => {
    // 获取当前行的数据（每一列的数据）
    return Object.values(data.cellData[rowIndex]).map(cell => cell.v);
  });
  return result;
}

import {ref,defineProps,defineEmits} from 'vue';
import {FWorkbook} from "@univerjs/sheets/facade";
const props=defineProps({
file:{type:Object,default:null},
new_file:{type:Object,default:null},
})
const emits=defineEmits(['data_change','close_sheet'])

const container = ref < HTMLElement | null > (null);
let univerAPIRef = reactive < Univer | null > (null);

const cell=csvtoWorkBook(props.file)
const fb=ref(null)
const workbook = ref({
  "id": "gyI0JO",
  "sheetOrder": [
    "RSfWjJFv4opmE1JaiRj80"
  ],
  "name": props.file.name,
  "appVersion": "0.5.0",
  "locale": "zhCN",
  "sheets": {
    "RSfWjJFv4opmE1JaiRj80": {
      "id": "RSfWjJFv4opmE1JaiRj80",
      "name": props.file.name,
      "rowCount": 50,
      "columnCount": 50,
      "scrollTop": 0,
      "scrollLeft": 0,
      "defaultColumnWidth": 75,
      "defaultRowHeight": 23,
      cellData: cell,
    }
  },

})

const loadFile=(file)=>
{
  cell.value=csvtoWorkBook(file)
  workbook.value.sheets.RSfWjJFv4opmE1JaiRj80.cellData=cell
  workbook.value.name=file.name
  workbook.value.sheets.RSfWjJFv4opmE1JaiRj80.name=file.name
  workbook.value={
  "id": "gyI0JO",
  "sheetOrder": [
    "RSfWjJFv4opmE1JaiRj80"
  ],
  "name": file.name,
  "appVersion": "0.5.0",
  "locale": "zhCN",
  "sheets": {
    "RSfWjJFv4opmE1JaiRj80": {
      "id": "RSfWjJFv4opmE1JaiRj80",
      "name": file.name,
      "rowCount": 50,
      "columnCount": 50,
      "scrollTop": 0,
      "scrollLeft": 0,
      "defaultColumnWidth": 75,
      "defaultRowHeight": 23,
      cellData: cell,
    }
  },

}

  fb.value=workbook.value
  // univerAPIRef.disposeUnit(univerAPIRef.getActiveWorkbook().id)
  // univerAPIRef.createWorkbook(workbook.value)
}
defineExpose({loadFile})
// const cell=ref(null)
// const workbb=ref({
//   id: props.file.name,
//   name: props.file.name,
//   appVersion: '1.0.0',
//   locale: 'zhCN',
//   sheetOrder: ['sheet1'],
//   sheets: {
//     sheet1: {
//   id: props.file.name+'11',
//   name: props.file.name,
//   tabColor: '#FF0000',
//   freeze: { xSplit: 1, ySplit: 1, startRow: 1, startColumn: 1 },
//   rowCount: 200,
//   columnCount: 100,
//   defaultColumnWidth: 75,
//   defaultRowHeight: 25,
//   cellData: {


//     '0': {
//       '0': {
//         v: 123
//       }
//     }
//   },
//   rowHeader: { width: 40 },
//   columnHeader: { height: 20 },
// },
//   }
// })
// const sheet=ref()

// workbb.value.sheets.sheet1=sheet
// cell.value=csvtoWorkBook(props.file)
// console.log(cell)
// console.log(workbook.value.sheets.RSfWjJFv4opmE1JaiRj80.cellData)
// workbook.value.sheets.RSfWjJFv4opmE1JaiRj80=cell.value

// sheet.value.cellData=csvtoWorkBook(props.file)

onMounted(() => {
  const {univerAPI:univerAPI} = createUniver({
    locale: LocaleType.ZH_CN,
    locales: {
      [LocaleType.ZH_CN]: merge(
          {},
          UniverPresetSheetsCoreZhCN,
      ),
    },
    theme: defaultTheme,
    presets: [
      UniverSheetsCorePreset({
        container: 'container'+props.file.name,
      }),
    ],
  });

//   workbook.value={
//   id: 'workbook1',
//   sheetOrder: ['sheet-01'],
//   sheets: {
//     'sheet-01': {
//       id: props.file.name,
//       name: props.file.name,
//       rowCount:100,
//       columnCount: 100,
//       cellData: {
//          0: { 0: { f: '=\'[workbook2]Sheet 01\'!A1' },1:{v:'a'}, }
//         // 0: {0:{v:1},1:{v:2}},
//         // 1:{0: {v:1},1:{v:2}}
//       }
//       //{ 0: { 0: { f: '=\'[workbook2]Sheet 01\'!A1' },1:{v:'a'}, } },
//     },
//   },
// }
  fb.value=univerAPI.createWorkbook(workbook.value);

  // univerAPI.createUnit(UniverInstanceType.UNIVER_SHEET, {})
  // console.log(workbook.value.cellData)
  univerAPIRef = univerAPI;
  // console.log(univerAPIRef)
});

onBeforeUnmount(() => {

  // emits('svaeChange',props.file,workBooktoCSV(univerAPIRef.getActiveWorkbook()))
  // toRaw(univerRef)?.dispose();
  toRaw(univerAPIRef).dispose();
  univerAPIRef = null;
});


</script>
<style scoped>

.excel_container{
  height: calc(100vh - 115px);
}
</style>