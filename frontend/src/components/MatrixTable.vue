<template>
  <div ref="container"></div>
</template>

<script setup>
import {onMounted, onBeforeUnmount, ref,reactive, toRaw} from 'vue'

import {createUniver, defaultTheme, LocaleType, merge} from '@univerjs/presets';
import {UniverSheetsCorePreset} from '@univerjs/presets/preset-sheets-core';
import UniverPresetSheetsCoreZhCN from '@univerjs/presets/preset-sheets-core/locales/zh-CN';
import {Univer} from "@univerjs/presets";
import '@univerjs/presets/lib/styles/preset-sheets-core.css';
import {Worksheet} from "@univerjs/presets";

const container = ref < HTMLElement | null > (null);
let univerAPIRef = reactive < Univer | null > (null);
const dat=ref({
  id: 'workbook1',
  sheetOrder: ['sheet-01'],
  sheets: {
    'sheet-01': {
      id: 'sheet-01',
      name: 'Sheet 01',
      rowCount: 10,
      columnCount: 5,
      cellData: { 0: { 0: { f: '=\'[workbook2]Sheet 01\'!A1' } } },
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
</script>