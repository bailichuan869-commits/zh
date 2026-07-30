import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SearchView from '@/views/SearchView.vue'
import DocumentView from '@/views/DocumentView.vue'
import RawFileView from '@/views/RawFileView.vue'

export default createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', component: HomeView },
    { path: '/search', component: SearchView },
    { path: '/document', component: DocumentView },
    { path: '/raw', component: RawFileView },
  ],
})
