<script setup lang="ts">
import { BulbOutlined, CloudOutlined, SearchOutlined } from '@ant-design/icons-vue'
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import { useTheme } from '@/composables/useTheme'

const router = useRouter()
const query = ref('')
const { dark, label, toggle } = useTheme()
function search() { if (query.value.trim()) router.push({ path: '/search', query: { q: query.value.trim() } }) }
</script>

<template>
  <a-layout class="shell">
    <a-layout-header class="header">
      <router-link class="brand" to="/">CPA-ZH <span>审计执业知识库</span></router-link>
      <a-input-search v-model:value="query" class="global-search" placeholder="检索法规、准则、案例和实务专题" @search="search">
        <template #enterButton><SearchOutlined /></template>
      </a-input-search>
      <a-tooltip :title="label"><a-button type="text" :aria-label="label" @click="toggle"><BulbOutlined v-if="dark" /><CloudOutlined v-else /></a-button></a-tooltip>
    </a-layout-header>
    <a-layout-content class="content"><slot /></a-layout-content>
  </a-layout>
</template>

<style scoped>
.shell { min-height: 100vh; background: var(--app-bg); }
.header { display: flex; align-items: center; gap: 24px; height: 60px; padding: 0 28px; background: var(--app-surface); border-bottom: 1px solid var(--app-border); }
.brand { color: var(--app-text); font-weight: 700; white-space: nowrap; }
.brand span { color: var(--app-muted); font-size: 12px; font-weight: 400; margin-left: 8px; }
.global-search { max-width: 580px; margin-left: auto; }
.content { padding: 28px; max-width: 1480px; width: 100%; margin: 0 auto; }
@media (max-width: 680px) { .header { padding: 0 14px; gap: 10px; } .brand span { display: none; } .content { padding: 16px; } }
</style>
