import { createRouter, createWebHashHistory } from 'vue-router'

export default createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', component: () => import('@/views/HomeView.vue') },
    { path: '/search', component: () => import('@/views/SearchView.vue') },
    { path: '/document', component: () => import('@/views/DocumentView.vue') },
    { path: '/raw', component: () => import('@/views/RawFileView.vue') },
    { path: '/answers', component: () => import('@/views/AnswerView.vue') },
    { path: '/maintenance', component: () => import('@/views/MaintenanceView.vue') },
    { path: '/ai-config', component: () => import('@/views/AIConfigView.vue') },
  ],
})
