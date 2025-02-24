<template>
  <div ref="container"></div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, toRaw } from 'vue'

import { createUniver, defaultTheme, LocaleType, merge } from '@univerjs/presets';
import { UniverSheetsCorePreset } from '@univerjs/presets/preset-sheets-core';
import UniverPresetSheetsCoreZhCN from '@univerjs/presets/preset-sheets-core/locales/zh-CN';
import {Univer} from "@univerjs/presets";
import '@univerjs/presets/lib/styles/preset-sheets-core.css';

const container = ref<HTMLElement | null>(null);
const univerAPIRef = ref<Univer | null>(null);

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
        container: container.value,
      }),
    ],
  });

  univerAPI.createWorkbook({ name: 'Test Sheet' });

  univerAPIRef.value = univerAPI;
});

onBeforeUnmount(() => {
  toRaw(univerRef.value)?.dispose();
  univerAPIRef.value = null;
});
</script>