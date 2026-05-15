import { createRouter, createWebHistory } from "vue-router";

import Layout from  "../layout/Layout.vue"

const routes = [
  {
    path: '/',
    component:Layout,
    redirect: '/dashboard',
    children:[
      {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('../views/Dashboard.vue'),
      meta: { title: '仪表盘' }
      },
      {
        path:'/invoice_test',
        name:'invoice_test',
        component:() => import('../views/InvoiceTest.vue'),
        meta: { title: '销售单(test)' }
      },
      {
      path:'/invoice',
      name:'invoice',
      component:() => import('../views/Invoice.vue'),
      meta: { title: '销售单' }
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;