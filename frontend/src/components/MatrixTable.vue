<template>

  <div ref="container"></div>
</template>

<script setup>
import {onMounted, onBeforeUnmount,reactive, toRaw} from 'vue'

import {createUniver, defaultTheme, LocaleType, merge} from '@univerjs/presets';
import {UniverSheetsCorePreset} from '@univerjs/presets/preset-sheets-core';
import UniverPresetSheetsCoreZhCN from '@univerjs/presets/preset-sheets-core/locales/zh-CN';
import {Univer} from "@univerjs/presets";
import '@univerjs/presets/lib/styles/preset-sheets-core.css';
import {Worksheet} from "@univerjs/presets";

import {ref,defineProps,defineEmits} from 'vue';
const props=defineProps({file:Object})
const emits=defineEmits(['data_change','close_sheet'])

const container = ref < HTMLElement | null > (null);
let univerAPIRef = reactive < Univer | null > (null);
const workbook=ref({
  id: 'workbook1',
  sheetOrder: ['sheet-01'],
  sheets: {
    'sheet-01': {
      id: file.name,
      name: file.name,
      rowCount: file.mat.length,
      columnCount: file.mat[0].length,
      cellData: {0: {0:{v:1},1:{v:2}},1:{0: {v:1},1:{v:2}}
      }
      //{ 0: { 0: { f: '=\'[workbook2]Sheet 01\'!A1' },1:{v:'a'}, } },
    },
  },
})

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
        container: container.value,
      }),
    ],
  });

  univerAPI.createWorkbook(dat.value);
  univerAPIRef = univerAPI;
  console.log(univerAPIRef)
});

onBeforeUnmount(() => {
  toRaw(univerRef.value)?.dispose();
  univerAPIRef = null;
});

const csvtoWorkBook=(file)=>{

  for(let row of file.mat)
  {

  }
}
const workBooktoCSV=(workbook)=>{

  for(let row of file.mat)
  {

  }
}

</script>