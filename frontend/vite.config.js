import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import vueDevTools from 'vite-plugin-vue-devtools'
const root = process.cwd();



// 所有页面
const pages = [
  { name: "index", htmlName: "index.html", htmlPath: "" },
  { name: "login", htmlName: "login.html", htmlPath: "./src/pages/login/" },
  { name: "register", htmlName: "register.html", htmlPath: "./src/pages/login/" },
  { name: "forgot", htmlName: "forgot.html", htmlPath: "./src/pages/login/" },
  { name: "home", htmlName: "index.html", htmlPath: "./src/pages/home/" },
  { name: "about", htmlName: "index.html", htmlPath: "./src/pages/about/" },
];

// pages.forEach((page) => {
//   page.path = pathResolve(page.htmlPath + page.htmlName);
// });
const multiplePagePlugin = () => ({
  name: "multiple-page-plugin",
  configureServer(server) {
    server.middlewares.use((req, res, next) => {
      for (let page of pages) {
        if (page.name === "index") {
          continue;
        }

        if (req.url.startsWith(`/${page.name}`)) {
          req.url = `/${page.htmlPath}${page.htmlName}`;
          break;
        }
      }
      next();
    });
  },
});

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    multiplePagePlugin(),
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
                // home: path.resolve(__dirname, 'home/index.html'),
                // login:path.resolve(__dirname,'src/pages/login/login.html'),


            },
        // input: pages.reduce((res, cur) => {
        //   res[cur.name] = cur.path;
        //   return res;
        // }, {}),
 output: {
                chunkFileNames: 'static/js/[name]-[hash].js',
                entryFileNames: "static/js/[name]-[hash].js",
                assetFileNames: "static/[ext]/name-[hash].[ext]"
            }
        },},

})

