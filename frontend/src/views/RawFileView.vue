<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { ArrowLeftOutlined, FileTextOutlined } from '@ant-design/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import MarkdownArticle from '@/components/MarkdownArticle.vue'
import {
  getRawFileName,
  getRawPreviewMode,
  isTextRawPreview,
  parseRawMarkdown,
} from '@/features/library/rawPreview'
import { api } from '@/services/api'

const route = useRoute()
const router = useRouter()
const path = computed(() => String(route.query.path ?? ''))
const previewMode = computed(() => getRawPreviewMode(path.value))
const previewUrl = computed(() => api.rawUrl(path.value))
const fileName = computed(() => getRawFileName(path.value))
const format = computed(() => {
  const name = fileName.value
  const extension = name.includes('.') ? name.split('.').pop()?.toUpperCase() : ''
  return extension || 'FILE'
})

const content = ref('')
const loading = ref(false)
const error = ref('')
let activeRequest = 0
const markdownDocument = computed(() =>
  previewMode.value === 'markdown'
    ? parseRawMarkdown(content.value)
    : { frontmatter: {}, markdown: content.value },
)
const isIndexPage = computed(() => markdownDocument.value.frontmatter.source_role === 'index-page')
const metadataEntries = computed(() => {
  const metadata = markdownDocument.value.frontmatter
  return [
    ['标题', metadata.title],
    ['来源类型', metadata.source_type],
    ['页面角色', metadata.source_role],
    ['原始文件', metadata.original_file],
  ].filter((entry): entry is [string, string] => Boolean(entry[1]))
})

const previewLabel = computed(() => {
  switch (previewMode.value) {
    case 'markdown':
      return '当前页渲染'
    case 'text':
      return '纯文本阅读'
    case 'html':
      return '内嵌 HTML'
    case 'pdf':
      return '内嵌 PDF'
    case 'image':
      return '内嵌图片'
    default:
      return '仅浏览'
  }
})

const previewHint = computed(() => {
  switch (previewMode.value) {
    case 'markdown':
      return 'Markdown 原文在当前页直接渲染，内部链接继续留在知识库内。'
    case 'text':
      return '纯文本在当前页展示，便于追溯和核验。'
    case 'html':
      return 'HTML 以受限预览方式嵌入当前页。'
    case 'pdf':
      return 'PDF 以当前页预览方式嵌入。'
    case 'image':
      return '图片文件直接嵌入当前页。'
    default:
      return '该格式暂不支持内嵌预览。'
  }
})

async function loadText() {
  if (!path.value || !isTextRawPreview(previewMode.value)) {
    activeRequest += 1
    content.value = ''
    error.value = ''
    loading.value = false
    return
  }

  const requestId = ++activeRequest
  loading.value = true
  error.value = ''

  try {
    const text = await api.rawText(path.value)
    if (requestId === activeRequest) content.value = text
  } catch (reason) {
    if (requestId !== activeRequest) return
    error.value = reason instanceof Error ? reason.message : '无法读取原始资料'
    content.value = ''
  } finally {
    if (requestId === activeRequest) loading.value = false
  }
}

function goBack() {
  if (window.history.state?.back) router.back()
  else router.push('/search')
}

watch([path, previewMode], loadText, { immediate: true })
</script>

<template>
  <a-spin :spinning="loading">
    <section v-if="!path" class="raw-state">
      <a-alert type="warning" message="请从检索结果中选择原始资料" show-icon />
    </section>

    <section v-else class="raw-layout">
      <main class="raw-main">
        <div class="raw-toolbar">
          <a-button type="text" class="back-button" aria-label="返回" @click="goBack">
            <ArrowLeftOutlined />返回
          </a-button>
        </div>

        <header class="raw-header">
          <p class="page-kicker">来源文件</p>
          <h1 class="page-heading">原始资料</h1>
          <p class="page-subheading source-path">{{ path }}</p>
        </header>

        <div class="action-row">
          <span>{{ previewHint }}</span>
        </div>

        <a-alert v-if="error" type="error" :message="error" show-icon class="notice">
          <template #action><a-button size="small" @click="loadText">重试</a-button></template>
        </a-alert>

        <a-alert
          v-if="previewMode === 'markdown' && isIndexPage"
          type="info"
          message="这是栏目索引页"
          description="本页用于追溯栏目列表；案例正文请打开表格中的本地正文页。"
          show-icon
          class="notice"
        />

        <div v-if="previewMode === 'markdown'" class="preview-shell">
          <MarkdownArticle :source="markdownDocument.markdown" />
        </div>

        <pre v-else-if="previewMode === 'text'" class="plain-preview">{{ content }}</pre>

        <iframe
          v-else-if="previewMode === 'html'"
          class="preview-frame"
          :src="previewUrl"
          title="原始 HTML 预览"
          sandbox="allow-same-origin"
        />

        <iframe
          v-else-if="previewMode === 'pdf'"
          class="preview-frame"
          :src="previewUrl"
          title="原始 PDF 预览"
        />

        <img
          v-else-if="previewMode === 'image'"
          class="preview-image"
          :src="previewUrl"
          :alt="fileName"
        />

        <div v-else class="file-notice">
          <span class="file-icon"><FileTextOutlined /></span>
          <div>
            <strong>当前格式暂不支持内嵌预览</strong>
            <p>知识库里已经保留了原始资料本体，这里只负责浏览。</p>
          </div>
        </div>
      </main>

      <aside class="raw-aside" aria-label="原始资料信息">
        <h2>文件信息</h2>
        <div class="info-line"><span>格式</span><strong>{{ format }}</strong></div>
        <div class="info-line"><span>浏览方式</span><strong>{{ previewLabel }}</strong></div>
        <div v-for="entry in metadataEntries" :key="entry[0]" class="info-line">
          <span>{{ entry[0] }}</span><strong class="metadata-value">{{ entry[1] }}</strong>
        </div>
        <div class="info-line"><span>来源路径</span><strong class="path-value">{{ path }}</strong></div>
      </aside>
    </section>
  </a-spin>
</template>

<style scoped>
.raw-state {
  width: min(840px, calc(100% - 40px));
  min-height: 220px;
  padding-top: 40px;
  margin: 0 auto;
}

.raw-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 240px;
  min-height: calc(100vh - var(--app-header-height));
  background: var(--reader-bg);
}

.raw-main {
  min-width: 0;
  padding: 18px clamp(28px, 5vw, 62px) 90px;
}

.raw-toolbar {
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
.action-row :deep(.anticon),
.file-icon :deep(.anticon),
.raw-aside :deep(.anticon) {
  font-size: var(--app-icon-size);
}

.raw-header {
  width: min(760px, 100%);
  margin: 34px auto 0;
}

.source-path {
  overflow-wrap: anywhere;
  font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
  font-size: 12px;
}

.action-row {
  width: min(760px, 100%);
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 14px;
  margin: 26px auto 18px;
}

.action-row span {
  color: var(--app-muted);
  font-size: 13px;
}

.notice {
  width: min(760px, 100%);
  margin: 0 auto 18px;
}

.preview-shell,
.plain-preview,
.preview-frame,
.preview-image,
.file-notice {
  width: min(760px, 100%);
  margin: 0 auto;
}

.preview-shell {
  color: var(--app-text);
}

.plain-preview {
  min-height: 70vh;
  padding: 18px 20px;
  overflow: auto;
  color: var(--app-text);
  white-space: pre-wrap;
  word-break: break-word;
  background: var(--app-surface);
  border: 1px solid var(--app-border);
  border-radius: 6px;
  font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
  font-size: 13px;
  line-height: 1.82;
}

.preview-frame {
  display: block;
  min-height: 70vh;
  background: var(--app-surface);
  border: 1px solid var(--app-border);
  border-radius: 6px;
}

.preview-image {
  display: block;
  max-height: 78vh;
  object-fit: contain;
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
  background: var(--reader-aside);
  border-left: 1px solid var(--reader-rule);
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

.metadata-value {
  overflow-wrap: anywhere;
}

@media (max-width: 1020px) {
  .raw-layout {
    grid-template-columns: 1fr;
  }

  .raw-aside {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 24px;
    padding: 24px clamp(28px, 5vw, 62px);
    border-top: 1px solid var(--reader-rule);
    border-left: 0;
  }

  .raw-aside h2 {
    grid-column: 1 / -1;
    margin: 0;
  }
}

@media (max-width: 680px) {
  .raw-main {
    padding: 14px 16px 54px;
  }

  .raw-header {
    margin-top: 24px;
  }

  .action-row {
    align-items: flex-start;
    flex-direction: column;
  }

  .preview-frame,
  .preview-image,
  .plain-preview,
  .file-notice {
    width: 100%;
  }

  .raw-aside {
    grid-template-columns: 1fr;
    padding: 24px 16px;
  }
}
</style>
