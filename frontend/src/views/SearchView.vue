<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { FilterOutlined, SearchOutlined } from '@ant-design/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import { isBrowsablePath } from '@/features/library/navigation'
import { cleanDisplayTitle, extractReadableTitle, isWeakTitle } from '@/features/library/titles'
import { api, type SearchResult } from '@/services/api'

interface DisplaySearchResult extends SearchResult {
  displayTitle: string
}

const route = useRoute()
const router = useRouter()
const query = ref(String(route.query.q ?? ''))
const domain = ref(String(route.query.domain ?? ''))
const kind = ref(String(route.query.kind ?? ''))
const profile = ref(String(route.query.profile ?? 'general-search'))
const asOf = ref(String(route.query.as_of ?? ''))
const results = ref<DisplaySearchResult[]>([])
const total = ref(0)
const facets = ref<[string, number][]>([])
const loading = ref(false)
const error = ref('')
const lastSearchKey = ref('')
const title = computed(() => query.value.trim() ? `找到 ${total.value} 条相关资料` : '输入关键词开始检索')
const profiles = [
  { value: 'general-search', label: '全库检索' },
  { value: 'answer-current', label: '当前有效答疑证据' },
  { value: 'case-review', label: '案例复核' },
  { value: 'learning', label: '学习对照' },
]

function makeSearchKey() {
  return [query.value.trim(), domain.value, kind.value, profile.value, asOf.value].join('\u0000')
}

async function run() {
  if (!query.value.trim()) {
    lastSearchKey.value = ''
    results.value = []
    total.value = 0
    return
  }

  lastSearchKey.value = makeSearchKey()
  loading.value = true
  error.value = ''
  try {
    const data = await api.search(query.value.trim(), domain.value, kind.value, 0, { profile: profile.value, as_of: asOf.value })
    const browsable = [...new Map(
      data.results.filter(item => isBrowsablePath(item.path)).map(item => [item.path, item]),
    ).values()]
    results.value = await Promise.all(browsable.map(async item => ({
      ...item,
      displayTitle: await resolveTitle(item),
    })))
    total.value = data.total
    facets.value = Object.entries(
      results.value.reduce<Record<string, number>>((counts, item) => {
        if (item.domain) counts[item.domain] = (counts[item.domain] ?? 0) + 1
        return counts
      }, {}),
    )
    router.replace({
      query: {
        q: query.value.trim(),
        ...(domain.value ? { domain: domain.value } : {}),
        ...(kind.value ? { kind: kind.value } : {}),
        ...(profile.value !== 'general-search' ? { profile: profile.value } : {}),
        ...(asOf.value ? { as_of: asOf.value } : {}),
      },
    })
  } catch (reason) {
    error.value = reason instanceof Error ? reason.message : '检索失败'
  } finally {
    loading.value = false
  }
}

async function resolveTitle(item: SearchResult): Promise<string> {
  const cleaned = cleanDisplayTitle(item.title, item.path)
  if (!isWeakTitle(cleaned) || !item.path.startsWith('raw/')) return cleaned || '未命名资料'

  try {
    const extracted = extractReadableTitle(await api.rawText(item.path))
    return extracted || cleaned || '未命名原始资料'
  } catch {
    return cleaned || '未命名原始资料'
  }
}

function open(item: SearchResult) {
  if (!isBrowsablePath(item.path)) return
  router.push({
    path: item.path.startsWith('wiki/') ? '/document' : '/raw',
    query: { path: item.path },
    ...(item.section_anchor ? { hash: `#${item.section_anchor}` } : {}),
  })
}

watch(
  () => [route.query.q, route.query.domain, route.query.kind, route.query.profile, route.query.as_of],
  value => {
    query.value = String(value[0] ?? '')
    domain.value = String(value[1] ?? '')
    kind.value = String(value[2] ?? '')
    profile.value = String(value[3] ?? 'general-search')
    asOf.value = String(value[4] ?? '')
    if (query.value.trim() && makeSearchKey() !== lastSearchKey.value) run()
    if (!query.value.trim()) {
      results.value = []
      total.value = 0
    }
  },
  { immediate: true },
)
</script>

<template>
  <section class="search-page">
    <header class="search-header">
      <p class="page-kicker">全库索引</p>
      <h1 class="page-heading">全文检索</h1>
      <p class="page-subheading">跨知识页面与原始资料检索，结果保留来源路径。</p>
      <a-input-search
        v-model:value="query"
        class="query-input"
        size="large"
        placeholder="输入关键词，例如：收入确认、函证、独立性"
        :loading="loading"
        allow-clear
        @search="run"
      >
        <template #prefix><SearchOutlined /></template>
        <template #enterButton><SearchOutlined />检索</template>
      </a-input-search>
    </header>

    <a-alert v-if="error" type="error" :message="error" show-icon class="result-alert">
      <template #action><a-button size="small" @click="run">重试</a-button></template>
    </a-alert>

    <div class="result-layout">
      <main class="result-section">
        <header class="result-heading">
          <h2>{{ title }}</h2>
          <span v-if="results.length">按相关性排序</span>
        </header>

        <a-spin :spinning="loading">
          <a-empty
            v-if="!loading && !results.length"
            :description="query.trim() ? '未找到匹配资料，请更换关键词或筛选条件' : '输入关键词开始检索'"
          />
          <a-list v-else class="result-list" :data-source="results" item-layout="vertical">
            <template #renderItem="{ item }">
              <a-list-item class="result-item">
                <button type="button" class="result-button" @click="open(item)">
                  <span class="result-copy">
                    <span class="result-top">
                      <strong>{{ item.displayTitle }}</strong>
                      <a-tag>{{ item.kind === 'wiki' ? '知识页面' : '原始资料' }}</a-tag>
                    </span>
                    <code class="result-path">{{ item.path }}</code>
                     <span class="result-snippet">{{ item.snippet }}</span>
                     <span class="result-tags">
                      <a-tag v-if="item.answer_ready" color="green">可用于答疑</a-tag>
                       <a-tag v-if="item.domain">{{ item.domain }}</a-tag>
                       <a-tag v-if="item.maturity">{{ item.maturity }}</a-tag>
                       <a-tag v-if="item.section">章节：{{ item.section }}</a-tag>
                       <a-tag v-if="item.version">版本：{{ item.version }}</a-tag>
                       <a-tag v-if="item.lifecycle_status">状态：{{ item.lifecycle_status }}</a-tag>
                     </span>
                  </span>
                  <span class="result-arrow" aria-hidden="true">›</span>
                </button>
              </a-list-item>
            </template>
          </a-list>
        </a-spin>
      </main>

      <aside class="filter-panel" aria-label="检索筛选">
        <div class="filter-title"><FilterOutlined />筛选范围</div>
        <label>
          <span>资料类型</span>
          <a-select v-model:value="kind" aria-label="资料类型" @change="run">
            <a-select-option value="">全部类型</a-select-option>
            <a-select-option value="wiki">知识页面</a-select-option>
            <a-select-option value="raw">原始资料</a-select-option>
          </a-select>
        </label>
        <label>
          <span>知识领域</span>
          <a-select v-model:value="domain" aria-label="知识领域" @change="run">
            <a-select-option value="">全部领域</a-select-option>
            <a-select-option v-for="facet in facets" :key="facet[0]" :value="facet[0]">
              {{ facet[0] }} ({{ facet[1] }})
            </a-select-option>
          </a-select>
        </label>
        <label>
          <span>检索策略</span>
          <a-select v-model:value="profile" aria-label="检索策略" @change="run">
            <a-select-option v-for="item in profiles" :key="item.value" :value="item.value">{{ item.label }}</a-select-option>
          </a-select>
        </label>
        <label>
          <span>截至日期</span>
          <a-input v-model:value="asOf" type="date" aria-label="截至日期" @change="run" />
        </label>
        <div class="filter-summary">
          <span>结果数量</span>
          <strong>{{ total }}</strong>
        </div>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.search-page {
  min-height: calc(100vh - var(--app-header-height));
  padding: 38px 42px 70px;
}

.search-header {
  width: min(860px, 100%);
}

.query-input {
  margin-top: 22px;
}

.query-input :deep(.ant-input-affix-wrapper) {
  min-height: 42px;
  padding-inline: 12px;
  background: var(--app-surface) !important;
}

.query-input :deep(.ant-input-search-button) {
  height: 42px;
  border-radius: 0 6px 6px 0 !important;
}

.query-input :deep(.anticon),
.filter-title :deep(.anticon) {
  font-size: var(--app-icon-size);
}

.result-alert {
  width: min(1100px, 100%);
  margin-top: 18px;
}

.result-layout {
  width: min(1100px, 100%);
  display: grid;
  grid-template-columns: minmax(0, 1fr) 220px;
  gap: 34px;
  align-items: start;
  margin-top: 30px;
}

.result-section {
  min-width: 0;
}

.result-heading {
  min-height: 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 7px;
}

.result-heading h2 {
  margin: 0;
  color: var(--app-text);
  font-size: 15px;
  font-weight: 500;
}

.result-heading span {
  color: var(--app-muted);
  font-size: 12px;
}

.result-list {
  background: transparent;
  border-top: 1px solid var(--app-border);
}

.result-item {
  padding: 0 !important;
  border-block-end: 1px solid var(--app-border) !important;
}

.result-button {
  width: 100%;
  min-width: 0;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 24px;
  gap: 12px;
  padding: 18px 10px;
  color: var(--app-text);
  background: transparent;
  border: 0;
  overflow: hidden;
  text-align: left;
  cursor: pointer;
}

.result-button:hover {
  background: var(--app-surface-hover);
}

.result-copy,
.result-top,
.result-snippet,
.result-tags {
  min-width: 0;
  display: flex;
}

.result-copy {
  flex-direction: column;
}

.result-top {
  align-items: flex-start;
  gap: 10px;
}

.result-top strong {
  min-width: 0;
  flex: 1;
  color: var(--app-text);
  font-size: 16px;
  font-weight: 500;
}

.result-path {
  max-width: 100%;
  display: block;
  margin-top: 6px;
  overflow: hidden;
  color: var(--app-subtle);
  font-size: 11px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.result-snippet {
  max-width: 100%;
  display: block;
  margin-top: 9px;
  color: var(--app-muted);
  overflow-wrap: anywhere;
  line-height: 1.72;
}

.result-tags {
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 11px;
}

.result-arrow {
  align-self: center;
  justify-self: center;
  color: var(--app-subtle);
  font-size: 20px;
}

.filter-panel {
  padding-left: 18px;
  border-left: 1px solid var(--app-border);
}

.filter-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 18px;
  color: var(--app-text);
  font-size: 15px;
  font-weight: 500;
}

.filter-panel label {
  display: block;
  margin-bottom: 16px;
}

.filter-panel label > span {
  display: block;
  margin-bottom: 7px;
  color: var(--app-muted);
  font-size: 12px;
}

.filter-panel :deep(.ant-select) {
  width: 100%;
}

.filter-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding-top: 16px;
  color: var(--app-muted);
  border-top: 1px solid var(--app-border);
  font-size: 12px;
}

.filter-summary strong {
  color: var(--app-text);
  font-size: 16px;
  font-weight: 500;
}

@media (max-width: 900px) {
  .result-layout {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .filter-panel {
    grid-row: 1;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
    padding: 0 0 18px;
    border-bottom: 1px solid var(--app-border);
    border-left: 0;
  }

  .filter-title,
  .filter-summary {
    grid-column: 1 / -1;
  }

  .filter-panel label {
    margin: 0;
  }
}

@media (max-width: 680px) {
  .search-page {
    padding: 28px 16px 48px;
  }

  .query-input :deep(.ant-input-search-button) {
    width: 42px;
    padding: 0;
    font-size: 0;
  }

  .filter-panel {
    grid-template-columns: 1fr;
  }

  .result-button {
    padding: 16px 4px;
  }

  .result-top {
    flex-wrap: wrap;
  }
}
</style>
