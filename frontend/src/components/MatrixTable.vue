<template>
  <div class="univer-container" ref="container"></div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, watch, reactive } from 'vue'
import { createUniver, defaultTheme, LocaleType, merge } from '@univerjs/presets'
import { UniverSheetsCorePreset } from '@univerjs/presets/preset-sheets-core'
import UniverPresetSheetsCoreZhCN from '@univerjs/presets/preset-sheets-core/locales/zh-CN'
import { Univer } from "@univerjs/presets"
import '@univerjs/presets/lib/styles/preset-sheets-core.css'

const props = defineProps({
  file: {
    type: Object,
    required: true,
    validator(value) {
      return 'name' in value && 'mat' in value
    }
  }
})

const emits = defineEmits({
  data_change: (data) => !!data,
  close_sheet: () => true,
  clipboard: (type) => ['copy','paste'].includes(type)
})

// 样式定义
const container = ref(null)
let univerAPIRef = reactive(null)

// 剪贴板功能
const handleCopy = (e) => {
  const selection = univerAPIRef.getActiveWorkbook().getActiveSheet().getSelection()
  const data = selection.getContent()
  navigator.clipboard.writeText(data)
  emits('clipboard', { type: 'copy', data })
  e.preventDefault()
}

const handlePaste = (e) => {
  navigator.clipboard.readText().then(text => {
    const data = parseCSV(text)
    const sheet = univerAPIRef.getActiveWorkbook().getActiveSheet()
    const { startRow, startCol } = sheet.getSelection().getPrimary()
    
    sheet.setRangeData({
      range: { 
        startRow,
        startCol,
        endRow: startRow + data.length - 1,
        endCol: startCol + data[0].length - 1
      },
      data
    })
    emits('clipboard', { type: 'paste', data })
  })
  e.preventDefault()
}

// CSV解析
const parseCSV = (text) => {
  return text.split('\n')
    .map(row => row.split(',').map(cell => cell.trim()))
}

// 数据加载
const loadData = (data) => {
  const workbook = univerAPIRef.getActiveWorkbook()
  const worksheet = workbook.getActiveSheet()
  
  if (data && data.length > 0) {
    // 清空现有数据
    worksheet.clear()
    
    // 设置新数据
    worksheet.setRowCount(data.length)
    worksheet.setColumnCount(data[0].length)
    worksheet.setRangeData({
      range: { 
        startRow: 0, 
        startCol: 0, 
        endRow: data.length-1, 
        endCol: data[0].length-1 
      },
      data
    })
    
    // 自动调整列宽
    worksheet.setColumnWidths(
      Array.from({length: data[0].length}, (_,i) => ({
        col: i,
        width: 150
      }))
    )
  }
}

// 初始化Univer实例
onMounted(() => {
  const { univerAPI } = createUniver({
    locale: LocaleType.ZH_CN,
    locales: {
      [LocaleType.ZH_CN]: merge({}, UniverPresetSheetsCoreZhCN)
    },
    theme: defaultTheme,
    presets: [
      UniverSheetsCorePreset({
        container: container.value,
      })
    ]
  })

  univerAPIRef = univerAPI
  const workbook = univerAPI.createWorkbook({
    id: 'workbook-' + Date.now(),
    sheetOrder: ['sheet-01'],
    sheets: {
      'sheet-01': {
        id: props.file.name,
        name: props.file.name,
        rowCount: props.file.mat.length,
        columnCount: props.file.mat[0].length,
        cellData: props.file.mat.reduce((acc, row, rowIdx) => {
          acc[rowIdx] = row.reduce((cellAcc, cell, colIdx) => {
            cellAcc[colIdx] = { v: cell }
            return cellAcc
          }, {})
          return acc
        }, {}),
        status: 1,
        selections: ['A1']
      }
    }
  })

  // 事件监听
  container.value.addEventListener('copy', handleCopy)
  container.value.addEventListener('paste', handlePaste)
  
  workbook.getActiveSheet().onCellContentChange((changes) => {
    changes.forEach(({ row, col, value }) => {
      props.file.mat[row][col] = value.v
    })
    emits('data_change', props.file)
  })
})

onBeforeUnmount(() => {
  if (univerAPIRef) {
    univerAPIRef.dispose()
    container.value.removeEventListener('copy', handleCopy)
    container.value.removeEventListener('paste', handlePaste)
  }
})

// 文件变化监听
watch(() => props.file, (newFile) => {
  if (newFile) {
    loadData(newFile.mat)
  }
})
</script>

<style scoped>
.univer-container {
  width: 100%;
  height: 600px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  margin: 20px 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
