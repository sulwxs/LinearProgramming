<template>
  <div ref="container" id="container" class="test"></div>


</template>

<script setup>
import {onMounted, onBeforeUnmount, ref, toRaw, reactive} from 'vue'

import { createUniver, defaultTheme, LocaleType, merge } from '@univerjs/presets';
import { UniverSheetsCorePreset } from '@univerjs/presets/preset-sheets-core';
import UniverPresetSheetsCoreZhCN from '@univerjs/presets/preset-sheets-core/locales/zh-CN';
import {Univer} from "@univerjs/presets";
import '@univerjs/presets/lib/styles/preset-sheets-core.css';

const container = ref<HTMLElement | null>(null);
let univerAPIRef = reactive < Univer | null > (null);

const workb=ref({
  id: 'sheet1111',
  name: '工作表 1111',
  tabColor: '#FF0000',
  freeze: { xSplit: 1, ySplit: 1, startRow: 1, startColumn: 1 },
  rowCount: 1000,
  columnCount: 26,
  defaultColumnWidth: 100,
  defaultRowHeight: 25,
  mergeData: [],
  cellData: {
    '0': {
      '0': {
        v: 123
      }
    }
  },
  rowData: [],
  columnData: [],
  rowHeader: { width: 40 },
  columnHeader: { height: 20 },
})

onMounted(() => {
  const { univerAPI } = createUniver({
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
        container: 'container',
      }),
    ],
  });

  univerAPI.createWorkbook(workb.value);


  univerAPIRef = univerAPI;
});

onBeforeUnmount(() => {
  toRaw(univerAPIRef)?.dispose();
  univerAPIRef = null;
});
const destroyUniver = () => {
  univer.value?.dispose();
  univer.value = null;
  workbook.value = null;
};
</script>
<style scoped>
.test{
 height: calc(100vh - 150px);
}
</style>