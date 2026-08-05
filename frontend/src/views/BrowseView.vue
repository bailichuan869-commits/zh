<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { ArrowRightOutlined, FileTextOutlined, FolderOpenOutlined } from '@ant-design/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import { getDomainMeta, orderDomains, sanitizeNavigationTree } from '@/features/library/navigation'
import { api, type NavigationDomain, type NavigationPage, type NavigationTopic, type NavigationTree } from '@/services/api'

const route = useRoute()
const router = useRouter()
const tree = ref<NavigationTree | null>(null)
const loading = ref(true)
const error = ref('')
const domainKey = ref('')
const topicKey = ref('')
const pageNumber = ref(1)
const pageSize = 30

const domains = computed(() => orderDomains(tree.value?.domains ?? []))
const selectedDomain = computed<NavigationDomain | null>(() =>
  domains.value.find(domain => domain.key === domainKey.value) ?? domains.value[0] ?? null,
)
const selectedTopic = computed<NavigationTopic | null>(() =>
  selectedDomain.value?.topics.find(topic => topic.key === topicKey.value) ?? selectedDomain.value?.topics[0] ?? null,
)
const visiblePages = computed(() => {
  const start = (pageNumber.value - 1) * pageSize
  return selectedTopic.value?.pages.slice(start, start + pageSize) ?? []
})

function applyRouteSelection() {
  if (!domains.value.length) return
  const requestedDomain = String(route.query.domain ?? '')
  const nextDomain = domains.value.find(domain => domain.key === requestedDomain) ?? domains.value[0]
  domainKey.value = nextDomain.key

  const requestedTopic = String(route.query.topic ?? '')
  const nextTopic = nextDomain.topics.find(topic => topic.key === requestedTopic) ?? nextDomain.topics[0]
  topicKey.value = nextTopic?.key ?? ''
  pageNumber.value = 1
}

async function load() {
  loading.value = true
  error.value = ''
  try {
    tree.value = sanitizeNavigationTree(await api.tree())
    applyRouteSelection()
  } catch (reason) {
    error.value = reason instanceof Error ? reason.message : '无法读取知识分类'
  } finally {
    loading.value = false
  }
}

function selectDomain(domain: NavigationDomain) {
  domainKey.value = domain.key
  topicKey.value = domain.topics[0]?.key ?? ''
  pageNumber.value = 1
  router.replace({ path: '/browse', query: { domain: domain.key, ...(topicKey.value ? { topic: topicKey.value } : {}) } })
}

function selectTopic(topic: NavigationTopic) {
  topicKey.value = topic.key
  pageNumber.value = 1
  router.replace({ path: '/browse', query: { domain: domainKey.value, topic: topic.key } })
}

function openPage(page: NavigationPage) {
  router.push({
    path: page.path.startsWith('wiki/') ? '/document' : '/raw',
    query: { path: page.path },
  })
}

watch(() => [route.query.domain, route.query.topic], applyRouteSelection)
onMounted(load)
</script>

<template>
  <section class="browse-page">
    <header class="browse-header">
      <div>
        <p class="page-kicker">知识目录</p>
        <h1 class="page-heading">分类浏览</h1>
        <p class="page-subheading">按照专业知识体系依次查看分类、主题和具体资料。</p>
      </div>
      <div v-if="tree" class="tree-state">
        <span class="app-status-dot" />{{ domains.length }} 个分类
      </div>
    </header>

    <a-alert v-if="error" type="error" :message="error" show-icon class="browse-alert">
      <template #action><a-button size="small" @click="load">重试</a-button></template>
    </a-alert>

    <a-spin :spinning="loading">
      <div v-if="tree && selectedDomain" class="browse-grid">
        <section class="browse-pane domain-pane" aria-labelledby="domain-title">
          <header class="pane-header">
            <h2 id="domain-title">知识分类</h2>
            <span>按体系排序</span>
          </header>
          <nav class="domain-list" aria-label="知识分类">
            <button
              v-for="(domain, index) in domains"
              :key="domain.key"
              type="button"
              :class="{ active: domain.key === selectedDomain.key }"
              @click="selectDomain(domain)"
            >
              <span class="domain-index">{{ String(index + 1).padStart(2, '0') }}</span>
              <span class="domain-copy">
                <strong>{{ domain.label }}</strong>
                <small>{{ domain.count }} 项</small>
              </span>
            </button>
          </nav>
        </section>

        <section class="browse-pane topic-pane" aria-labelledby="topic-title">
          <header class="pane-header">
            <h2 id="topic-title">{{ selectedDomain.label }}</h2>
            <component :is="getDomainMeta(selectedDomain.key).icon" />
          </header>
          <nav class="topic-list" aria-label="主题分类">
            <button
              v-for="topic in selectedDomain.topics"
              :key="topic.key"
              type="button"
              :class="{ active: topic.key === selectedTopic?.key }"
              @click="selectTopic(topic)"
            >
              <span>{{ topic.label }}</span><small>{{ topic.count }}</small>
            </button>
          </nav>
        </section>

        <main class="page-pane">
          <header class="page-pane-header">
            <div>
              <p>{{ selectedDomain.label }}</p>
              <h2>{{ selectedTopic?.label || '暂无主题' }}</h2>
            </div>
            <span>{{ selectedTopic?.count ?? 0 }} 项资料</span>
          </header>

          <a-empty v-if="!selectedTopic?.pages.length" description="该主题暂无可浏览资料" />
          <div v-else class="page-list">
            <button v-for="page in visiblePages" :key="page.path" type="button" @click="openPage(page)">
              <span class="page-icon">
                <FileTextOutlined v-if="page.path.startsWith('wiki/')" />
                <FolderOpenOutlined v-else />
              </span>
              <span class="page-copy">
                <strong>{{ page.title }}</strong>
                <small>{{ page.path }}</small>
                <span class="page-meta">
                  <span>{{ page.path.startsWith('wiki/') ? '知识页面' : '原始资料' }}</span>
                  <span v-if="page.updated">更新于 {{ page.updated }}</span>
                  <span v-if="page.maturity">{{ page.maturity }}</span>
                </span>
              </span>
              <ArrowRightOutlined />
            </button>
          </div>

          <a-pagination
            v-if="(selectedTopic?.count ?? 0) > pageSize"
            v-model:current="pageNumber"
            class="page-pagination"
            :page-size="pageSize"
            :total="selectedTopic?.count ?? 0"
            :show-size-changer="false"
            size="small"
          />
        </main>
      </div>
    </a-spin>
  </section>
</template>

<style scoped>
.browse-page {
  min-height: calc(100vh - var(--app-header-height));
  padding: 34px 36px 64px;
}

.browse-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
}

.tree-state {
  min-height: 34px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--app-muted);
  font-size: 12px;
}

.browse-alert {
  margin-top: 20px;
}

.browse-grid {
  display: grid;
  grid-template-columns: 216px 238px minmax(0, 1fr);
  min-height: 600px;
  margin-top: 28px;
  border-top: 1px solid var(--app-border);
  border-bottom: 1px solid var(--app-border);
}

.browse-pane {
  min-width: 0;
  padding: 18px 14px 20px 0;
  border-right: 1px solid var(--app-border);
}

.topic-pane {
  padding-left: 14px;
}

.pane-header,
.page-pane-header {
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}

.pane-header h2,
.page-pane-header h2 {
  margin: 0;
  color: var(--app-text);
  font-size: 15px;
  font-weight: 500;
}

.pane-header span,
.pane-header :deep(.anticon),
.page-pane-header > span {
  color: var(--app-muted);
  font-size: 12px;
}

.pane-header :deep(.anticon),
.page-list :deep(.anticon) {
  font-size: var(--app-icon-size);
}

.domain-list,
.topic-list {
  display: grid;
  gap: 2px;
}

.domain-list button,
.topic-list button {
  width: 100%;
  color: var(--app-muted);
  background: transparent;
  border: 0;
  border-radius: 6px;
  text-align: left;
  cursor: pointer;
}

.domain-list button:hover,
.topic-list button:hover {
  color: var(--app-text);
  background: var(--app-surface-hover);
}

.domain-list button.active,
.topic-list button.active {
  color: var(--app-text);
  background: var(--app-surface-subtle);
}

.domain-list button {
  min-height: 52px;
  display: grid;
  grid-template-columns: 30px minmax(0, 1fr);
  align-items: center;
  gap: 9px;
  padding: 7px 8px;
}

.domain-index {
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  color: var(--app-subtle);
  border: 1px solid var(--app-border);
  border-radius: 5px;
  font-size: 11px;
}

.domain-copy,
.domain-copy strong,
.domain-copy small {
  min-width: 0;
  display: block;
}

.domain-copy strong {
  overflow: hidden;
  color: inherit;
  font-size: 13px;
  font-weight: 500;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.domain-copy small {
  margin-top: 2px;
  color: var(--app-subtle);
  font-size: 11px;
}

.topic-list button {
  min-height: 38px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 10px;
  padding: 7px 9px;
}

.topic-list button span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.topic-list button small {
  color: var(--app-subtle);
  font-size: 11px;
}

.page-pane {
  min-width: 0;
  padding: 18px 0 24px 18px;
}

.page-pane-header p {
  margin: 0 0 3px;
  color: var(--app-muted);
  font-size: 11px;
}

.page-list {
  border-top: 1px solid var(--app-border);
}

.page-list button {
  width: 100%;
  min-height: 76px;
  display: grid;
  grid-template-columns: 34px minmax(0, 1fr) 20px;
  align-items: center;
  gap: 12px;
  padding: 12px 8px;
  color: var(--app-text);
  background: transparent;
  border: 0;
  border-bottom: 1px solid var(--app-border);
  text-align: left;
  cursor: pointer;
}

.page-list button:hover {
  background: var(--app-surface-hover);
}

.page-icon {
  width: 32px;
  height: 32px;
  display: grid;
  place-items: center;
  color: var(--app-accent-text);
  background: var(--app-accent-soft);
  border-radius: 6px;
}

.page-copy,
.page-copy strong,
.page-copy small {
  min-width: 0;
  display: block;
}

.page-copy strong {
  overflow: hidden;
  font-weight: 500;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.page-copy small {
  margin-top: 4px;
  overflow: hidden;
  color: var(--app-subtle);
  font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
  font-size: 10px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.page-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 9px;
  margin-top: 6px;
  color: var(--app-muted);
  font-size: 11px;
}

.page-list button > :deep(.anticon) {
  justify-self: center;
  color: var(--app-subtle);
}

.page-pagination {
  display: flex;
  justify-content: flex-end;
  margin-top: 18px;
}

@media (max-width: 1100px) {
  .browse-grid {
    grid-template-columns: 190px 210px minmax(0, 1fr);
  }
}

@media (max-width: 900px) {
  .browse-grid {
    display: block;
  }

  .browse-pane {
    padding: 16px 0;
    border-right: 0;
    border-bottom: 1px solid var(--app-border);
  }

  .domain-list,
  .topic-list {
    display: flex;
    gap: 4px;
    overflow-x: auto;
    padding-bottom: 4px;
    scrollbar-width: none;
  }

  .domain-list::-webkit-scrollbar,
  .topic-list::-webkit-scrollbar {
    display: none;
  }

  .domain-list button {
    min-width: 174px;
  }

  .topic-list button {
    min-width: 170px;
  }

  .page-pane {
    padding-left: 0;
  }
}

@media (max-width: 680px) {
  .browse-page {
    padding: 28px 16px 48px;
  }

  .browse-header {
    align-items: flex-start;
    flex-direction: column;
    gap: 6px;
  }

  .browse-grid {
    margin-top: 20px;
  }

  .page-list button {
    grid-template-columns: 32px minmax(0, 1fr) 16px;
    gap: 9px;
    padding-inline: 4px;
  }
}
</style>
