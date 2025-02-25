import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import vueDevTools from 'vite-plugin-vue-devtools'
// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),

  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@page':fileURLToPath(new URL('./src/pages',import.meta.url)),
    },
  },
  build: {
        rollupOptions: {
            input: {
                index: path.resolve(__dirname, 'index.html'),
                home: path.resolve(__dirname, './home/index.html'),
            }, output: {
                chunkFileNames: 'static/js/[name]-[hash].js',
                entryFileNames: "static/js/[name]-[hash].js",
                assetFileNames: "static/[ext]/name-[hash].[ext]"
            }
        },},

})
