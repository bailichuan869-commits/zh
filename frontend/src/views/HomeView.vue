<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import {
  AppstoreOutlined,
  ArrowRightOutlined,
  BookOutlined,
  DashboardOutlined,
  FileSearchOutlined,
  FileTextOutlined,
  SafetyCertificateOutlined,
} from '@ant-design/icons-vue'
import { useRouter } from 'vue-router'
import { getDomainMeta, orderDomains, sanitizeNavigationTree } from '@/features/library/navigation'
import { api, type NavigationTree, type Summary } from '@/services/api'

const router = useRouter()
const summary = ref<Summary | null>(null)
const tree = ref<NavigationTree | null>(null)
const loading = ref(true)
const error = ref('')

const domains = computed(() => orderDomains(tree.value?.domains ?? []))
const featuredDomains = computed(() => domains.value.slice(0, 8))
const generatedAt = computed(() => {
  if (!tree.value?.generated) return '-'
  const value = new Date(tree.value.generated)
  return Number.isNaN(value.getTime()) ? tree.value.generated : value.toLocaleString('zh-CN', { hour12: false })
})

const tools = [
  { title: '分类浏览', desc: '按分类、主题和资料顺序查看', path: '/browse', icon: AppstoreOutlined },
  { title: '全文检索', desc: '跨知识页面与原始资料定位关键词', path: '/search', icon: FileSearchOutlined },
  { title: '知识库状态', desc: '检查索引、页面和关联关系', path: '/health', icon: DashboardOutlined },
]

async function load() {
  loading.value = true
  error.value = ''
  try {
    const [summaryData, treeData] = await Promise.all([api.summary(), api.tree()])
    summary.value = summaryData
    tree.value = sanitizeNavigationTree(treeData)
  } catch (reason) {
    error.value = reason instanceof Error ? reason.message : '无法读取知识库总览'
  } finally {
    loading.value = false
  }
}

function openDomain(key: string) {
  router.push({ path: '/browse', query: { domain: key } })
}

onMounted(load)
</script>

<template>
  <main class="dashboard-page">
    <header class="dashboard-header">
      <div>
        <p class="page-kicker">中国 CPA 专业知识库</p>
        <h1 class="page-heading">知识库总览</h1>
        <p class="page-subheading">从专业分类进入知识体系，或使用工作功能定位具体资料。</p>
      </div>
      <router-link to="/health" class="dashboard-status">
        <span class="app-status-dot" />只读索引已连接
      </router-link>
    </header>

    <a-alert v-if="error" type="error" :message="error" show-icon class="dashboard-alert">
      <template #action><a-button size="small" @click="load">重试</a-button></template>
    </a-alert>

    <a-spin :spinning="loading">
      <section class="metric-strip" aria-label="知识库数据概览">
        <div class="metric-item">
          <BookOutlined />
          <span>结构化知识页面</span>
          <strong>{{ summary?.wiki_pages ?? '-' }}</strong>
        </div>
        <div class="metric-item">
          <FileTextOutlined />
          <span>全库索引资料</span>
          <strong>{{ summary?.total ?? '-' }}</strong>
        </div>
        <div class="metric-item">
          <SafetyCertificateOutlined />
          <span>已复核内容</span>
          <strong>{{ summary?.answer_ready ?? '-' }}</strong>
        </div>
        <div class="metric-item">
          <AppstoreOutlined />
          <span>可浏览分类</span>
          <strong>{{ domains.length || '-' }}</strong>
        </div>
      </section>

      <div class="dashboard-grid">
        <section class="domain-panel" aria-labelledby="domain-panel-title">
          <header class="section-heading">
            <div>
              <p>知识体系</p>
              <h2 id="domain-panel-title">分类入口</h2>
            </div>
            <a-button type="text" @click="router.push('/browse')">查看全部<ArrowRightOutlined /></a-button>
          </header>

          <div class="domain-grid">
            <button v-for="domain in featuredDomains" :key="domain.key" type="button" @click="openDomain(domain.key)">
              <span class="domain-icon"><component :is="getDomainMeta(domain.key).icon" /></span>
              <span class="domain-copy">
                <strong>{{ domain.label }}</strong>
                <small>{{ getDomainMeta(domain.key).description }}</small>
              </span>
              <span class="domain-count">{{ domain.count }}</span>
              <ArrowRightOutlined />
            </button>
          </div>
        </section>

        <aside class="dashboard-side">
          <section class="tool-panel" aria-labelledby="tool-panel-title">
            <header class="section-heading">
              <div>
                <p>操作入口</p>
                <h2 id="tool-panel-title">工作功能</h2>
              </div>
            </header>
            <div class="tool-list">
              <button v-for="tool in tools" :key="tool.path" type="button" @click="router.push(tool.path)">
                <component :is="tool.icon" />
                <span><strong>{{ tool.title }}</strong><small>{{ tool.desc }}</small></span>
                <ArrowRightOutlined />
              </button>
            </div>
          </section>

          <section class="state-panel" aria-labelledby="state-panel-title">
            <header class="section-heading">
              <div>
                <p>当前服务</p>
                <h2 id="state-panel-title">运行状态</h2>
              </div>
            </header>
            <div class="state-row"><span>检索索引</span><strong>已连接</strong></div>
            <div class="state-row"><span>Web 界面</span><strong>只读</strong></div>
            <div class="state-row"><span>分类树更新</span><strong>{{ generatedAt }}</strong></div>
          </section>
        </aside>
      </div>
    </a-spin>
  </main>
</template>

<style scoped>
.dashboard-page {
  min-height: calc(100vh - var(--app-header-height));
  padding: 38px 42px 64px;
}

.dashboard-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
}

.dashboard-status {
  min-height: 34px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--app-muted);
  font-size: 12px;
  text-decoration: none;
}

.dashboard-alert {
  margin-top: 20px;
}

.metric-strip {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  margin-top: 28px;
  border-top: 1px solid var(--app-border);
  border-bottom: 1px solid var(--app-border);
}

.metric-item {
  min-width: 0;
  min-height: 86px;
  display: grid;
  grid-template-columns: 24px minmax(0, 1fr);
  grid-template-rows: auto auto;
  align-content: center;
  gap: 4px 8px;
  padding: 14px 18px;
  border-right: 1px solid var(--app-border);
}

.metric-item:last-child {
  border-right: 0;
}

.metric-item > :deep(.anticon) {
  grid-row: 1 / 3;
  align-self: center;
  color: var(--app-muted);
  font-size: var(--app-icon-size);
}

.metric-item span {
  overflow: hidden;
  color: var(--app-muted);
  font-size: 12px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.metric-item strong {
  color: var(--app-text);
  font-size: 22px;
  font-weight: 500;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.65fr) minmax(280px, 0.75fr);
  gap: 40px;
  margin-top: 34px;
}

.section-heading {
  min-height: 44px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 10px;
}

.section-heading p {
  margin: 0 0 3px;
  color: var(--app-muted);
  font-size: 11px;
}

.section-heading h2 {
  margin: 0;
  color: var(--app-text);
  font-size: 16px;
  font-weight: 500;
}

.section-heading :deep(.ant-btn) {
  color: var(--app-muted);
}

.section-heading :deep(.anticon),
.domain-grid :deep(.anticon),
.tool-list :deep(.anticon) {
  font-size: var(--app-icon-size);
}

.domain-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  border-top: 1px solid var(--app-border);
}

.domain-grid button {
  min-width: 0;
  min-height: 82px;
  display: grid;
  grid-template-columns: 36px minmax(0, 1fr) auto 18px;
  align-items: center;
  gap: 11px;
  padding: 12px 10px;
  color: var(--app-text);
  background: transparent;
  border: 0;
  border-right: 1px solid var(--app-border);
  border-bottom: 1px solid var(--app-border);
  text-align: left;
  cursor: pointer;
}

.domain-grid button:nth-child(even) {
  border-right: 0;
}

.domain-grid button:hover,
.tool-list button:hover {
  background: var(--app-surface-hover);
}

.domain-icon {
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  color: var(--app-accent-text);
  background: var(--app-accent-soft);
  border-radius: 6px;
}

.domain-copy,
.domain-copy strong,
.domain-copy small {
  min-width: 0;
  display: block;
}

.domain-copy strong {
  font-weight: 500;
}

.domain-copy small {
  margin-top: 4px;
  overflow: hidden;
  color: var(--app-muted);
  font-size: 11px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.domain-count {
  color: var(--app-muted);
  font-size: 12px;
}

.domain-grid button > :deep(.anticon),
.tool-list button > :deep(.anticon:last-child) {
  color: var(--app-subtle);
}

.dashboard-side {
  min-width: 0;
  display: grid;
  align-content: start;
  gap: 30px;
}

.tool-list {
  border-top: 1px solid var(--app-border);
}

.tool-list button {
  width: 100%;
  min-height: 64px;
  display: grid;
  grid-template-columns: 26px minmax(0, 1fr) 18px;
  align-items: center;
  gap: 10px;
  padding: 10px 7px;
  color: var(--app-text);
  background: transparent;
  border: 0;
  border-bottom: 1px solid var(--app-border);
  text-align: left;
  cursor: pointer;
}

.tool-list button > :deep(.anticon:first-child) {
  color: var(--app-muted);
}

.tool-list button span,
.tool-list strong,
.tool-list small {
  min-width: 0;
  display: block;
}

.tool-list strong {
  font-weight: 500;
}

.tool-list small {
  margin-top: 3px;
  color: var(--app-muted);
  font-size: 11px;
}

.state-panel {
  border-top: 1px solid var(--app-border);
}

.state-row {
  min-height: 40px;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  align-items: start;
  gap: 14px;
  padding: 10px 0;
  color: var(--app-muted);
  border-bottom: 1px solid var(--app-border);
  font-size: 12px;
}

.state-row strong {
  min-width: 0;
  color: var(--app-text);
  font-weight: 500;
  text-align: right;
  overflow-wrap: anywhere;
}

@media (max-width: 1080px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .dashboard-side {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 780px) {
  .metric-strip,
  .domain-grid,
  .dashboard-side {
    grid-template-columns: 1fr;
  }

  .metric-item,
  .domain-grid button {
    border-right: 0;
  }
}

@media (max-width: 680px) {
  .dashboard-page {
    padding: 28px 16px 48px;
  }

  .dashboard-header {
    align-items: flex-start;
    flex-direction: column;
    gap: 6px;
  }

  .metric-strip {
    margin-top: 22px;
  }

  .dashboard-grid {
    gap: 28px;
    margin-top: 28px;
  }

  .domain-grid button {
    grid-template-columns: 34px minmax(0, 1fr) auto 16px;
    gap: 9px;
    padding-inline: 4px;
  }
}
</style>
