import { createRouter, createWebHashHistory } from 'vue-router'

export default createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', component: () => import('@/views/HomeView.vue') },
    { path: '/browse', component: () => import('@/views/BrowseView.vue') },
    { path: '/search', component: () => import('@/views/SearchView.vue') },
    { path: '/document', component: () => import('@/views/DocumentView.vue') },
    { path: '/raw', component: () => import('@/views/RawFileView.vue') },
    { path: '/health', component: () => import('@/views/HealthView.vue') },
    { path: '/answers', redirect: '/' },
    { path: '/maintenance', redirect: '/' },
    { path: '/ai-config', redirect: '/' },
  ],
})
