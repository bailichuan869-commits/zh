<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { ArrowLeftOutlined, LinkOutlined } from '@ant-design/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import MarkdownArticle from '@/components/MarkdownArticle.vue'
import { api, type Document } from '@/services/api'

const route = useRoute()
const router = useRouter()
const document = ref<Document | null>(null)
const loading = ref(false)
const error = ref('')
const path = computed(() => String(route.query.path ?? ''))
const displayTitle = computed(() => document.value?.frontmatter.title || document.value?.path || '')

async function load() {
  if (!path.value) return
  loading.value = true
  error.value = ''
  try {
    document.value = await api.document(path.value)
  } catch (reason) {
    error.value = reason instanceof Error ? reason.message : '无法读取知识页面'
  } finally {
    loading.value = false
  }
}

function openBacklink(target: string) {
  router.push({ path: '/document', query: { path: `wiki/${target}.md` } })
}

watch(path, load, { immediate: true })
</script>

<template>
  <a-spin :spinning="loading">
    <section v-if="error" class="document-state">
      <a-alert type="error" :message="error" show-icon>
        <template #action><a-button size="small" @click="load">重试</a-button></template>
      </a-alert>
    </section>

    <section v-else-if="document" class="reading-layout">
      <main class="article-main">
        <div class="article-toolbar">
          <a-button type="text" class="back-button" aria-label="返回上一页" @click="router.back()">
            <ArrowLeftOutlined />返回
          </a-button>
          <span class="article-path">{{ document.path }}</span>
        </div>

        <article class="article-content">
          <header class="article-header">
            <p class="page-kicker">{{ document.frontmatter.type || '知识页面' }}</p>
            <h1>{{ displayTitle }}</h1>
            <div class="article-meta">
              <a-tag v-if="document.frontmatter.maturity" color="green">{{ document.frontmatter.maturity }}</a-tag>
              <a-tag v-if="document.frontmatter.page_role">{{ document.frontmatter.page_role }}</a-tag>
              <span>{{ document.backlinks.length }} 条关联知识</span>
            </div>
          </header>

          <div class="article-rule" />
          <MarkdownArticle :source="document.markdown" />
        </article>
      </main>

      <aside class="article-aside" aria-label="文档上下文">
        <section>
          <h2>页面信息</h2>
          <div class="info-line"><span>文档类型</span><strong>{{ document.frontmatter.type || '知识页面' }}</strong></div>
          <div class="info-line"><span>成熟度</span><strong>{{ document.frontmatter.maturity || '已整理' }}</strong></div>
          <div class="info-line"><span>来源路径</span><strong class="path-value">{{ document.path }}</strong></div>
        </section>

        <section class="backlink-section">
          <h2><LinkOutlined />关联页面</h2>
          <a-empty v-if="!document.backlinks.length" :image="null" description="暂无关联页面" />
          <div v-else class="backlink-list">
            <button v-for="item in document.backlinks" :key="item.path" type="button" @click="openBacklink(item.path)">
              <span>{{ item.title }}</span><span aria-hidden="true">›</span>
            </button>
          </div>
        </section>
      </aside>
    </section>

    <section v-else-if="!loading" class="document-state">
      <a-empty description="请选择要阅读的知识页面" />
    </section>
  </a-spin>
</template>

<style scoped>
.reading-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 240px;
  min-height: calc(100vh - var(--app-header-height));
  background: var(--reader-bg);
}

.article-main {
  min-width: 0;
  padding: 18px clamp(28px, 5vw, 62px) 90px;
}

.article-toolbar {
  min-height: 34px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--app-muted);
}

.back-button {
  height: 32px;
  padding-inline: 8px;
  color: var(--app-muted);
}

.back-button :deep(.anticon),
.article-aside :deep(.anticon) {
  font-size: var(--app-icon-size);
}

.article-path {
  min-width: 0;
  overflow: hidden;
  font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
  font-size: 11px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.article-content {
  width: min(760px, 100%);
  margin: 34px auto 0;
}

.article-header h1 {
  margin: 6px 0 13px;
  color: var(--app-text);
  font-size: 34px;
  line-height: 1.28;
  font-weight: 500;
  letter-spacing: 0;
}

.article-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 7px;
  color: var(--app-muted);
  font-size: 12px;
}

.article-rule {
  height: 1px;
  margin: 23px 0 30px;
  background: var(--app-border);
}

.article-content :deep(.markdown-article > h1:first-child) {
  display: none;
}

.article-aside {
  padding: 28px 16px;
  background: var(--reader-aside);
  border-left: 1px solid var(--reader-rule);
}

.article-aside section {
  padding-bottom: 22px;
  margin-bottom: 22px;
  border-bottom: 1px solid var(--app-border);
}

.article-aside h2 {
  display: flex;
  align-items: center;
  gap: 7px;
  margin: 0 0 12px;
  color: var(--app-text);
  font-size: 15px;
  font-weight: 500;
}

.info-line {
  min-height: 38px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  padding: 9px 0;
  color: var(--app-muted);
  border-bottom: 1px solid var(--app-border);
  font-size: 12px;
}

.info-line:last-child {
  border-bottom: 0;
}

.info-line strong {
  min-width: 0;
  color: var(--app-text);
  font-weight: 500;
  text-align: right;
}

.path-value {
  overflow-wrap: anywhere;
}

.backlink-section :deep(.ant-empty) {
  margin-block: 18px;
}

.backlink-section :deep(.ant-empty-description) {
  color: var(--app-muted);
  font-size: 12px;
}

.backlink-list {
  border-top: 1px solid var(--app-border);
}

.backlink-list button {
  width: 100%;
  min-height: 40px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 14px;
  align-items: center;
  gap: 8px;
  padding: 8px 6px;
  color: var(--app-muted);
  background: transparent;
  border: 0;
  border-bottom: 1px solid var(--app-border);
  text-align: left;
  cursor: pointer;
}

.backlink-list button:hover {
  color: var(--app-text);
  background: var(--app-surface-hover);
}

.backlink-list button span:first-child {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.document-state {
  width: min(840px, calc(100% - 40px));
  min-height: 320px;
  padding-top: 40px;
  margin: 0 auto;
}

@media (max-width: 1020px) {
  .reading-layout {
    grid-template-columns: 1fr;
  }

  .article-aside {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 24px;
    padding: 24px clamp(28px, 5vw, 62px);
    border-top: 1px solid var(--reader-rule);
    border-left: 0;
  }

  .article-aside section {
    margin: 0;
  }
}

@media (max-width: 680px) {
  .article-main {
    padding: 14px 16px 54px;
  }

  .article-content {
    margin-top: 24px;
  }

  .article-header h1 {
    font-size: 28px;
  }

  .article-aside {
    grid-template-columns: 1fr;
    padding: 24px 16px;
  }
}
</style>
