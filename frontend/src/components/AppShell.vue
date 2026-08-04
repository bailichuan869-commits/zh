<script setup lang="ts">
import { ApiOutlined, BookOutlined, BulbOutlined, HomeOutlined, QuestionCircleOutlined, SearchOutlined, SettingOutlined, ToolOutlined } from '@ant-design/icons-vue'
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTheme } from '@/composables/useTheme'

const router = useRouter(); const route = useRoute(); const query = ref(String(route.query.q ?? ''))
const { dark, label, toggle } = useTheme()
const nav = [
  { path: '/', label: '首页', icon: HomeOutlined },
  { path: '/search', label: '全文检索', icon: SearchOutlined },
  { path: '/answers', label: '知识问答', icon: QuestionCircleOutlined },
  { path: '/maintenance', label: '维护更新', icon: ToolOutlined },
  { path: '/ai-config', label: 'AI 配置', icon: SettingOutlined },
]
function search() { const q = query.value.trim(); if (q) router.push({ path: '/search', query: { q } }) }
</script>
<template>
  <a-layout class="app-frame">
    <header class="topbar">
      <router-link to="/" class="brand"><span class="brand-symbol"><BookOutlined /></span><strong>CPA-ZH</strong></router-link>
      <span class="workspace-chip">专业工作台</span>
      <a-input-search v-model:value="query" class="top-search" placeholder="搜索法规、准则、案例和实务专题" @search="search"><template #prefix><SearchOutlined /></template><template #enterButton><span>搜索</span></template></a-input-search>
      <router-link to="/answers"><a-button type="primary" shape="round"><ApiOutlined />AI 助手</a-button></router-link>
      <a-tooltip :title="label"><a-button class="theme-toggle" type="text" shape="circle" :aria-label="label" @click="toggle"><BulbOutlined /></a-button></a-tooltip>
      <span class="avatar">CPA</span>
    </header>
    <a-layout class="body-layout">
      <a-layout-sider class="sidebar" width="236">
        <span class="nav-label">工作区</span>
        <nav><a-tooltip v-for="item in nav" :key="item.path" :title="item.label" placement="right"><a-button type="text" block class="nav-item" :aria-label="item.label" :class="{ active: route.path === item.path }" @click="router.push(item.path)"><component :is="item.icon" /><span>{{ item.label }}</span></a-button></a-tooltip></nav>
        <div class="nav-divider" />
        <span class="nav-label">知识范围</span>
        <div class="scope-note"><BookOutlined /><div><strong>CPA-ZH</strong><small>法规、准则、案例与实务</small></div></div>
        <div class="sidebar-foot"><span class="health-dot" />本地索引已连接</div>
      </a-layout-sider>
      <a-layout-content class="page-content"><slot /></a-layout-content>
    </a-layout>
  </a-layout>
</template>
<style scoped>
.app-frame { min-height:100vh; }.topbar { position:sticky; top:0; z-index:10; display:flex; align-items:center; gap:14px; height:66px; padding:0 22px; background:var(--app-surface-raised); border-bottom:1px solid var(--app-border); backdrop-filter:blur(22px) saturate(1.35); }.brand { display:flex; align-items:center; gap:10px; color:var(--app-text); font-size:17px; white-space:nowrap; }.brand-symbol { display:grid; place-items:center; width:34px; height:34px; color:#fff; background:linear-gradient(145deg,#1672ee,#022e72); border-radius:10px; box-shadow:0 6px 16px rgba(0,74,180,.22); }.workspace-chip { padding:6px 10px; color:var(--app-muted); background:var(--app-code); border:1px solid var(--app-border); border-radius:999px; font-size:12px; white-space:nowrap; }.top-search { max-width:720px; margin-right:auto; }.top-search :deep(.ant-input-affix-wrapper) { border-radius:999px 0 0 999px !important; }.top-search :deep(.ant-input-search-button) { border-radius:0 999px 999px 0 !important; }.theme-toggle { color:var(--app-muted); }.avatar { display:grid; place-items:center; width:34px; height:34px; color:#fff; background:var(--app-accent); border-radius:50%; font-size:10px; font-weight:700; }.body-layout { min-height:calc(100vh - 66px); }.sidebar { position:sticky; top:66px; height:calc(100vh - 66px); padding:22px 14px; background:var(--app-sidebar) !important; border-right:1px solid var(--app-border); }.nav-label { display:block; margin:0 9px 8px; color:var(--app-subtle); font-size:11px; }.nav-item { display:flex; align-items:center; gap:11px; height:42px; margin:2px 0; padding:0 12px; color:var(--app-muted); text-align:left; }.nav-item.active { color:var(--app-accent); background:var(--app-accent-soft); font-weight:650; }.nav-item :deep(.anticon) { font-size:16px; }.nav-divider { height:1px; margin:18px 8px; background:var(--app-border); }.scope-note { display:flex; align-items:center; gap:10px; padding:12px; color:var(--app-text); background:var(--app-code); border:1px solid var(--app-border); border-radius:10px; }.scope-note :deep(.anticon) { color:var(--app-accent); }.scope-note strong,.scope-note small { display:block; }.scope-note small { margin-top:3px; color:var(--app-muted); font-size:10px; }.sidebar-foot { position:absolute; bottom:20px; left:24px; color:var(--app-muted); font-size:11px; }.health-dot { display:inline-block; width:7px; height:7px; margin-right:7px; background:#27b99a; border-radius:50%; }.page-content { min-width:0; }@media(max-width:850px) { .workspace-chip,.avatar { display:none; }.topbar { padding:0 12px; gap:8px; }.brand strong { display:none; }.top-search { min-width:0; }.sidebar { width:72px !important; flex:0 0 72px !important; max-width:72px !important; min-width:72px !important; padding:18px 8px; }.nav-label,.nav-item span,.scope-note div,.sidebar-foot { display:none; }.nav-item { justify-content:center; padding:0; }.scope-note { justify-content:center; padding:12px 0; } }@media(max-width:540px) { .topbar>a:nth-of-type(2),.theme-toggle { display:none; } }
</style>
