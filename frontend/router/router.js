// router.js
import { createRouter, createWebHistory } from 'vue-router';

// 引入Vue组件
import MatrixViews from "@/components/MatrixViews.vue";
import upload from "@/components/upload.vue";
import LinearProgrammingForm from "@/components/LinearProgrammingForm.vue";
import ProjectManager from "@/components/projectManager.vue";
// 定义路由
const routes = [
    { path: '/matrixview', component: MatrixViews,props:true },
    { path: '/fileManage', component: upload,props:true  },
    { path: '/solver', component: LinearProgrammingForm,props:true  },
    { path: '/projects', component: ProjectManager,props:true  },
];

// 创建router实例
const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;