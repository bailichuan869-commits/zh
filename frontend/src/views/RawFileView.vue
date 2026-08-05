<script setup lang="ts">
import { computed } from 'vue'
import { ArrowLeftOutlined, DownloadOutlined, FileTextOutlined } from '@ant-design/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '@/services/api'

const route = useRoute()
const router = useRouter()
const path = computed(() => String(route.query.path ?? ''))
const url = computed(() => api.rawUrl(path.value))
const isHtml = computed(() => /\.html?$/i.test(path.value))
const format = computed(() => path.value.split('.').pop()?.toUpperCase() || 'FILE')

function goBack() {
  if (window.history.state?.back) router.back()
  else router.push('/search')
}
</script>

<template>
  <section class="raw-layout">
    <main class="raw-main">
      <div class="raw-toolbar">
        <a-button type="text" class="back-button" aria-label="返回" @click="goBack">
          <ArrowLeftOutlined />返回
        </a-button>
      </div>

      <header class="raw-header">
        <p class="page-kicker">来源文件</p>
        <h1 class="page-heading">原始资料</h1>
        <p class="page-subheading source-path">{{ path || '请选择要查看的原始资料' }}</p>
      </header>

      <a-alert v-if="!path" type="warning" message="请从检索结果中选择原始资料" show-icon class="notice" />
      <template v-else>
        <div class="action-row">
          <a :href="url" target="_blank" rel="noopener">
            <a-button type="primary"><DownloadOutlined />在新窗口打开</a-button>
          </a>
          <span>原始资料由后端受限提供，阅读页不改写原文件。</span>
        </div>

        <iframe v-if="isHtml" class="preview" :src="url" title="原始 HTML 预览" sandbox="allow-same-origin" />
        <div v-else class="file-notice">
          <span class="file-icon"><FileTextOutlined /></span>
          <div><strong>此文件可在独立窗口中查看或下载</strong><p>支持原始资料的追溯与核验；请通过上方操作打开文件。</p></div>
        </div>
      </template>
    </main>

    <aside class="raw-aside" aria-label="原始资料信息">
      <h2>文件信息</h2>
      <div class="info-line"><span>格式</span><strong>{{ format }}</strong></div>
      <div class="info-line"><span>访问方式</span><strong>只读</strong></div>
      <div class="info-line"><span>来源路径</span><strong class="path-value">{{ path || '-' }}</strong></div>
    </aside>
  </section>
</template>

<style scoped>
.raw-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 240px;
  min-height: calc(100vh - var(--app-header-height));
}

.raw-main {
  min-width: 0;
  padding: 18px 42px 70px;
}

.raw-toolbar {
  min-height: 34px;
  display: flex;
  align-items: center;
  margin-bottom: 18px;
}

.back-button {
  height: 32px;
  padding-inline: 8px;
  color: var(--app-muted);
}

.back-button :deep(.anticon) {
  font-size: var(--app-icon-size);
}

.source-path {
  overflow-wrap: anywhere;
  font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
  font-size: 12px;
}

.notice {
  margin-top: 24px;
}

.action-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 14px;
  margin: 26px 0 18px;
}

.action-row :deep(.anticon),
.file-icon :deep(.anticon),
.raw-aside :deep(.anticon) {
  font-size: var(--app-icon-size);
}

.action-row span {
  color: var(--app-muted);
  font-size: 13px;
}

.preview {
  width: 100%;
  min-height: 70vh;
  display: block;
  background: var(--app-surface);
  border: 1px solid var(--app-border);
  border-radius: 6px;
}

.file-notice {
  min-height: 100px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 20px;
  background: var(--app-surface);
  border: 1px solid var(--app-border);
  border-radius: 8px;
}

.file-icon {
  width: 32px;
  height: 32px;
  display: grid;
  place-items: center;
  flex: 0 0 32px;
  color: var(--app-accent-text);
  background: var(--app-accent-soft);
  border-radius: 6px;
}

.file-notice strong {
  display: block;
  font-weight: 500;
}

.file-notice p {
  margin: 5px 0 0;
  color: var(--app-muted);
  font-size: 13px;
}

.raw-aside {
  padding: 28px 16px;
  background: var(--app-sidebar);
  border-left: 1px solid var(--app-border);
}

.raw-aside h2 {
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

.info-line strong {
  min-width: 0;
  color: var(--app-text);
  font-weight: 500;
  text-align: right;
}

.path-value {
  overflow-wrap: anywhere;
}

@media (max-width: 900px) {
  .raw-layout {
    grid-template-columns: 1fr;
  }

  .raw-aside {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 18px;
    padding: 24px 42px;
    border-top: 1px solid var(--app-border);
    border-left: 0;
  }

  .raw-aside h2 {
    grid-column: 1 / -1;
    margin: 0;
  }
}

@media (max-width: 680px) {
  .raw-main {
    padding: 14px 16px 48px;
  }

  .action-row {
    align-items: flex-start;
    flex-direction: column;
  }

  .raw-aside {
    grid-template-columns: 1fr;
    padding: 24px 16px;
  }
}
</style>
