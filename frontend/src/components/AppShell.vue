<script setup lang="ts">
import {
  AppstoreOutlined,
  AuditOutlined,
  BankOutlined,
  BookOutlined,
  BulbFilled,
  BulbOutlined,
  DashboardOutlined,
  FileSearchOutlined,
  HomeOutlined,
  ProfileOutlined,
  SearchOutlined,
  SafetyCertificateOutlined,
} from '@ant-design/icons-vue'
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTheme } from '@/composables/useTheme'

const router = useRouter()
const route = useRoute()
const query = ref(String(route.query.q ?? ''))
const quickSearchOpen = ref(false)
const { dark, setTheme } = useTheme()

const primaryNav = [
  { path: '/', label: '首页', icon: HomeOutlined },
  { path: '/browse', label: '分类浏览', icon: AppstoreOutlined },
  { path: '/search', label: '全文检索', icon: FileSearchOutlined },
  { path: '/health', label: '知识库状态', icon: DashboardOutlined },
]

const scopeNav = [
  { key: 'laws', label: '法律法规', icon: BankOutlined },
  { key: 'accounting-standards', label: '会计准则', icon: BookOutlined },
  { key: 'audit-standards', label: '审计准则', icon: AuditOutlined },
  { key: 'policies', label: '监管政策', icon: ProfileOutlined },
  { key: 'ethics', label: '职业道德', icon: SafetyCertificateOutlined },
]

const pageLabel = computed(() => {
  if (route.path === '/') return '知识库总览'
  if (route.path === '/document') return '知识阅读'
  if (route.path === '/raw') return '原始资料'
  return primaryNav.find(item => item.path === route.path)?.label ?? '知识页面'
})

watch(
  () => route.query.q,
  value => {
    if (route.path === '/search') query.value = String(value ?? '')
  },
)

function search() {
  const value = query.value.trim()
  if (!value) return
  quickSearchOpen.value = false
  router.push({ path: '/search', query: { q: value } })
}

function openScope(key: string) {
  router.push({ path: '/browse', query: { domain: key } })
}
</script>

<template>
  <a-layout class="app-frame">
    <header class="topbar">
      <router-link to="/" class="brand" aria-label="返回 CPA-ZH 知识库首页">
        <span class="brand-symbol"><BookOutlined /></span>
        <span class="brand-name">CPA-ZH 知识库</span>
      </router-link>

      <div class="page-context">
        <span>中国注册会计师 · 本地知识工作台</span>
        <strong>{{ pageLabel }}</strong>
      </div>

      <div class="top-actions">
        <a-tooltip title="搜索知识库">
          <a-button type="text" class="quick-search-button" aria-label="搜索知识库" @click="quickSearchOpen = true">
            <SearchOutlined />
          </a-button>
        </a-tooltip>
        <router-link to="/health" class="sync-state">
          <span class="app-status-dot" />索引已连接
        </router-link>
        <div class="theme-control" role="group" aria-label="外观主题">
          <a-tooltip title="浅色模式">
            <a-button
              type="text"
              class="theme-button"
              :class="{ active: !dark }"
              aria-label="浅色模式"
              :aria-pressed="!dark"
              @click="setTheme(false)"
            ><BulbOutlined /></a-button>
          </a-tooltip>
          <a-tooltip title="深色模式">
            <a-button
              type="text"
              class="theme-button"
              :class="{ active: dark }"
              aria-label="深色模式"
              :aria-pressed="dark"
              @click="setTheme(true)"
            ><BulbFilled /></a-button>
          </a-tooltip>
        </div>
      </div>
    </header>

    <nav class="mobile-nav" aria-label="主导航">
      <button
        v-for="item in primaryNav"
        :key="item.path"
        type="button"
        :class="{ active: route.path === item.path }"
        @click="router.push(item.path)"
      >
        <component :is="item.icon" />{{ item.label }}
      </button>
    </nav>

    <a-layout class="body-layout">
      <a-layout-sider class="sidebar" :width="204">
        <div class="workspace-block">
          <span class="workspace-name">中国注册会计师</span>
          <span class="workspace-kind">本地知识工作台</span>
        </div>

        <nav class="sidebar-nav" aria-label="知识库导航">
          <a-button
            v-for="item in primaryNav"
            :key="item.path"
            type="text"
            block
            class="nav-item"
            :class="{ active: route.path === item.path }"
            @click="router.push(item.path)"
          >
            <component :is="item.icon" />
            <span>{{ item.label }}</span>
          </a-button>
        </nav>

        <div class="nav-label">专业分类</div>
        <nav class="sidebar-nav scope-nav" aria-label="专业分类">
          <a-button
            v-for="item in scopeNav"
            :key="item.key"
            type="text"
            block
            class="nav-item"
            :class="{ active: route.path === '/browse' && route.query.domain === item.key }"
            @click="openScope(item.key)"
          >
            <component :is="item.icon" />
            <span>{{ item.label }}</span>
          </a-button>
        </nav>

        <router-link to="/health" class="sidebar-foot">
          <span class="app-status-dot" />
          <span><strong>只读服务正常</strong><small>索引与页面已连接</small></span>
        </router-link>
      </a-layout-sider>

      <a-layout-content class="page-content"><slot /></a-layout-content>
    </a-layout>

    <a-modal v-model:open="quickSearchOpen" title="搜索知识库" :footer="null" width="560px">
      <a-input-search
        v-model:value="query"
        autofocus
        size="large"
        placeholder="输入关键词，例如：收入确认、函证、独立性"
        enter-button="检索"
        @search="search"
      >
        <template #prefix><SearchOutlined /></template>
      </a-input-search>
    </a-modal>
  </a-layout>
</template>

<style scoped>
.app-frame {
  min-height: 100vh;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 20;
  display: grid;
  grid-template-columns: var(--app-sidebar-width) minmax(0, 1fr) auto;
  align-items: center;
  gap: 16px;
  min-height: var(--app-header-height);
  padding: 10px 14px;
  background: var(--app-surface-raised);
  border-bottom: 1px solid var(--app-border);
}

.brand {
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--app-text);
  font-weight: 500;
  text-decoration: none;
}

.brand-symbol {
  width: 30px;
  height: 30px;
  flex: 0 0 30px;
  display: grid;
  place-items: center;
  color: var(--app-surface);
  background: var(--app-text);
  border-radius: 7px;
}

.brand-symbol :deep(.anticon),
.top-actions :deep(.anticon),
.sidebar :deep(.anticon),
.mobile-nav :deep(.anticon) {
  font-size: var(--app-icon-size);
}

.brand-name {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.page-context {
  min-width: 0;
}

.page-context span,
.page-context strong {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.page-context span {
  color: var(--app-subtle);
  font-size: 11px;
}

.page-context strong {
  margin-top: 2px;
  color: var(--app-text);
  font-size: 13px;
  font-weight: 500;
}

.top-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
}

.quick-search-button,
.theme-button {
  width: 30px;
  height: 28px;
  padding: 0;
  color: var(--app-muted);
  border-radius: 5px;
}

.quick-search-button:hover,
.theme-button:hover {
  color: var(--app-text) !important;
  background: var(--app-surface-hover) !important;
}

.sync-state {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  margin-left: 3px;
  color: var(--app-muted);
  font-size: 12px;
  text-decoration: none;
  white-space: nowrap;
}

.theme-control {
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 3px;
  background: var(--app-surface-subtle);
  border-radius: 7px;
}

.theme-button.active {
  color: var(--app-text);
  background: var(--app-surface);
  box-shadow: var(--app-shadow-soft);
}

.body-layout {
  min-height: calc(100vh - var(--app-header-height));
}

.sidebar {
  position: sticky !important;
  top: var(--app-header-height);
  height: calc(100vh - var(--app-header-height));
  padding: 14px 10px;
  overflow: hidden auto;
  background: var(--app-sidebar) !important;
  border-right: 1px solid var(--app-border);
}

.workspace-block {
  padding: 7px 8px 13px;
  margin-bottom: 10px;
  border-bottom: 1px solid var(--app-border);
}

.workspace-name,
.workspace-kind {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.workspace-name {
  color: var(--app-text);
  font-weight: 500;
}

.workspace-kind {
  margin-top: 2px;
  color: var(--app-muted);
  font-size: 12px;
}

.sidebar-nav {
  display: grid;
  gap: 2px;
}

.nav-label {
  padding: 18px 9px 6px;
  color: var(--app-subtle);
  font-size: 11px;
}

.nav-item {
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 9px;
  padding: 0 9px;
  color: var(--app-muted);
  text-align: left;
  border-radius: 6px;
}

.nav-item:hover {
  color: var(--app-text) !important;
  background: var(--app-surface-hover) !important;
}

.nav-item.active {
  color: var(--app-text);
  background: var(--app-surface-subtle);
  font-weight: 500;
}

.sidebar-foot {
  position: absolute;
  right: 10px;
  bottom: 14px;
  left: 10px;
  display: grid;
  grid-template-columns: 10px minmax(0, 1fr);
  align-items: start;
  gap: 8px;
  padding: 10px 9px;
  color: var(--app-muted);
  border-top: 1px solid var(--app-border);
  text-decoration: none;
}

.sidebar-foot .app-status-dot {
  margin-top: 5px;
}

.sidebar-foot strong,
.sidebar-foot small {
  display: block;
}

.sidebar-foot strong {
  color: var(--app-text);
  font-size: 12px;
  font-weight: 500;
}

.sidebar-foot small {
  margin-top: 2px;
  color: var(--app-subtle);
  font-size: 11px;
}

.page-content {
  min-width: 0;
}

.mobile-nav {
  display: none;
}

@media (max-width: 980px) {
  .topbar {
    grid-template-columns: 184px minmax(0, 1fr) auto;
  }

  .sync-state {
    display: none;
  }

  .sidebar {
    width: 184px !important;
    min-width: 184px !important;
    max-width: 184px !important;
    flex: 0 0 184px !important;
  }
}

@media (max-width: 680px) {
  .topbar {
    position: static;
    grid-template-columns: minmax(0, 1fr) auto;
    gap: 8px;
    padding: 10px 12px;
  }

  .page-context {
    display: none;
  }

  .sidebar {
    display: none;
  }

  .body-layout {
    min-height: 0;
  }

  .mobile-nav {
    display: flex;
    gap: 4px;
    padding: 7px 10px;
    overflow-x: auto;
    scrollbar-width: none;
    background: var(--app-sidebar);
    border-bottom: 1px solid var(--app-border);
  }

  .mobile-nav::-webkit-scrollbar {
    display: none;
  }

  .mobile-nav button {
    min-height: 34px;
    flex: 0 0 auto;
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 0 9px;
    color: var(--app-muted);
    background: transparent;
    border: 0;
    border-radius: 5px;
  }

  .mobile-nav button.active {
    color: var(--app-text);
    background: var(--app-surface-subtle);
  }
}
</style>
