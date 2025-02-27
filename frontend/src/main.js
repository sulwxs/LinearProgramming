// import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import VueExcelEditor from 'vue3-excel-editor'

import VueKatex from 'vue3-katex'
import 'katex/dist/katex.min.css'

import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import router from "../router/router";
import 'element-plus/theme-chalk/display.css'
const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.use(VueKatex)
app.use(VueExcelEditor)
app.use(ElementPlus)
app.use(router)
app.mount('#app')
