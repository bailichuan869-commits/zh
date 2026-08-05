<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import type { UploadProps } from 'ant-design-vue'
import {
  ArrowLeftOutlined,
  CheckOutlined,
  DeleteOutlined,
  EyeOutlined,
  FileMarkdownOutlined,
  FileTextOutlined,
  InboxOutlined,
  UploadOutlined,
} from '@ant-design/icons-vue'
import {
  api,
  type IngestUploadItem,
  type MaintenancePreview,
  type MaintenanceResult,
  type PendingReview,
  type PendingReviewDetail,
} from '@/services/api'

type Mode = 'ingest' | 'qa' | 'review'

const mode = ref<Mode>('ingest')
const token = ref('')
const preview = ref<MaintenancePreview | null>(null)
const result = ref<MaintenanceResult | null>(null)
const error = ref('')
const actionLoading = ref(false)
const uploadLoading = ref(false)
const commitLoading = ref(false)
const pendingReviews = ref<PendingReview[]>([])
const selectedReview = ref('')
const reviewStep = ref<1 | 2>(1)
const selectedReviewDetail = ref<PendingReviewDetail | null>(null)
const reviewDetailComplete = ref(false)
const reviewDetailLoading = ref(false)
const reviewConfirmed = ref(false)
const uploadSession = ref('')
const ingestItems = ref<IngestUploadItem[]>([])
const markdownOpen = ref(false)
const markdownLoading = ref(false)
const markdownTitle = ref('')
const markdownContent = ref('')
const qa = reactive({ question: '', answer: '', title: '', slug: '', source: 'local-qa-log', tags: '', related: '' })
let uploadTimer: ReturnType<typeof setTimeout> | undefined
let selectedFiles: File[] = []

const resultSubtitle = computed(() => result.value?.health.startsWith('demo:')
  ? '开发模拟已完成，未写入知识库或执行维护命令。'
  : '文件已入库，缓存、索引与健康检查均已刷新。')
const canCommitIngest = computed(() => ingestItems.value.length > 0
  && ingestItems.value.every(item => item.batch_name.trim().length > 0))
const tableColumns = [
  { title: '原始文件', key: 'file', width: 250 },
  { title: '提取 MD 预览', key: 'markdown', width: 430 },
  { title: '批次名称', key: 'batch', width: 280 },
  { title: '', key: 'actions', width: 54, fixed: 'right' as const },
]

function requireToken() {
  if (token.value.trim()) return true
  error.value = '请输入本机维护令牌'
  return false
}

const beforeUpload: UploadProps['beforeUpload'] = (_file, fileList) => {
  selectedFiles = fileList as unknown as File[]
  if (uploadTimer) clearTimeout(uploadTimer)
  uploadTimer = setTimeout(() => void parseFiles([...selectedFiles]), 0)
  return false
}

async function parseFiles(files: File[]) {
  if (!requireToken() || !files.length) return
  uploadLoading.value = true
  error.value = ''
  result.value = null
  preview.value = null
  try {
    const response = await api.uploadIngest(files, token.value.trim())
    uploadSession.value = response.session_token
    ingestItems.value = response.items
  } catch (reason) {
    error.value = reason instanceof Error ? reason.message : '文件解析失败'
  } finally {
    uploadLoading.value = false
    selectedFiles = []
  }
}

function removeIngestItem(id: string) {
  ingestItems.value = ingestItems.value.filter(item => item.id !== id)
}

async function showMarkdown(item: IngestUploadItem) {
  markdownOpen.value = true
  markdownTitle.value = item.filename
  markdownContent.value = item.markdown_preview
  if (!item.preview_truncated) return
  markdownLoading.value = true
  try {
    markdownContent.value = (await api.uploadedMarkdown(uploadSession.value, item.id, token.value.trim())).markdown
  } catch (reason) {
    error.value = reason instanceof Error ? reason.message : '无法读取完整 Markdown'
  } finally {
    markdownLoading.value = false
  }
}

async function commitIngest() {
  if (!requireToken() || !canCommitIngest.value || !uploadSession.value) return
  commitLoading.value = true
  error.value = ''
  try {
    result.value = await api.commitUploadedIngest(
      uploadSession.value,
      ingestItems.value.map(item => ({ id: item.id, batch_name: item.batch_name.trim() })),
      token.value.trim(),
    )
    uploadSession.value = ''
    ingestItems.value = []
  } catch (reason) {
    error.value = reason instanceof Error ? reason.message : '批量入库失败'
  } finally {
    commitLoading.value = false
  }
}

async function createPreview() {
  if (!requireToken()) return
  if (mode.value === 'review' && !reviewConfirmed.value) {
    error.value = '请先阅读页面正文和来源，并勾选已完成专业复核'
    return
  }
  const review = pendingReviews.value.find(item => item.path === selectedReview.value)
  actionLoading.value = true
  error.value = ''
  result.value = null
  preview.value = null
  try {
    preview.value = mode.value === 'qa'
      ? await api.previewQa({ ...qa }, token.value.trim())
      : await api.previewReview(selectedReview.value, review?.content_sha256 ?? '', reviewConfirmed.value, token.value.trim())
  } catch (reason) {
    error.value = reason instanceof Error ? reason.message : '无法生成预览'
  } finally {
    actionLoading.value = false
  }
}

async function selectReview(item: PendingReview) {
  selectedReview.value = item.path
  reviewStep.value = 2
  reviewConfirmed.value = false
  preview.value = null
  result.value = null
  error.value = ''
  selectedReviewDetail.value = {
    path: item.path,
    title: item.title,
    page_role: item.page_role,
    maturity: item.maturity,
    raw_path: item.raw_path,
    body: item.body_preview,
    content_sha256: item.content_sha256,
  }
  reviewDetailComplete.value = false
  reviewDetailLoading.value = true
  try {
    selectedReviewDetail.value = await api.reviewDetail(item.path, token.value.trim())
    reviewDetailComplete.value = true
  } catch (reason) {
    // Older maintenance processes do not expose the detail route yet; use the existing read API as a compatibility fallback.
    try {
      const document = await api.document(item.path)
      selectedReviewDetail.value = {
        path: item.path,
        title: document.frontmatter.title || item.title,
        page_role: item.page_role,
        maturity: item.maturity,
        raw_path: item.raw_path,
        body: document.markdown,
        content_sha256: item.content_sha256,
      }
      reviewDetailComplete.value = true
    } catch {
      error.value = reason instanceof Error ? reason.message : '无法读取页面详情'
    }
  } finally {
    reviewDetailLoading.value = false
  }
}

function handleReviewChange() {
  reviewStep.value = 1
  reviewConfirmed.value = false
  selectedReviewDetail.value = null
  reviewDetailComplete.value = false
  preview.value = null
}

function completeReview() {
  if (!selectedReview.value || !reviewDetailComplete.value) return
  reviewConfirmed.value = true
  reviewStep.value = 1
  error.value = ''
}

async function commitPreview() {
  if (!preview.value) return
  actionLoading.value = true
  error.value = ''
  try {
    result.value = mode.value === 'qa'
      ? await api.commitQa({ ...qa }, preview.value.preview_token, token.value.trim())
      : await api.commitReview(selectedReview.value, preview.value.review?.content_sha256 ?? '', reviewConfirmed.value, preview.value.preview_token, token.value.trim())
    preview.value = null
    if (mode.value === 'review') await loadPendingReviews()
  } catch (reason) {
    error.value = reason instanceof Error ? reason.message : '提交失败'
  } finally {
    actionLoading.value = false
  }
}

async function loadPendingReviews() {
  if (!requireToken()) return
  actionLoading.value = true
  error.value = ''
  try {
    pendingReviews.value = (await api.pendingReviews(token.value.trim())).items
    if (!pendingReviews.value.some(item => item.path === selectedReview.value)) {
      selectedReview.value = ''
    }
    reviewStep.value = 1
    selectedReviewDetail.value = null
    reviewDetailComplete.value = false
    reviewConfirmed.value = false
  } catch (reason) {
    error.value = reason instanceof Error ? reason.message : '无法读取待复核队列'
  } finally {
    actionLoading.value = false
  }
}

function formatSize(bytes: number) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`
}

function ingestRowKey(item: IngestUploadItem) {
  return item.id
}
</script>

<template>
  <section class="maintenance-page">
    <header class="page-header">
      <div>
        <h1 class="page-heading">知识库维护</h1>
        <p class="page-subheading">导入资料、沉淀问答并确认待复核知识页。</p>
      </div>
      <a-input-password v-model:value="token" class="token-input" autocomplete="off" placeholder="维护令牌" />
    </header>

    <a-tabs v-model:active-key="mode" class="maintenance-tabs" @change="preview = null; result = null; error = ''">
      <a-tab-pane key="ingest" tab="资料导入">
        <div class="ingest-workspace">
          <a-upload-dragger
            accept=".md,.txt,.csv,.html,.htm,.xml,.docx,.pdf"
            :before-upload="beforeUpload"
            :disabled="uploadLoading || commitLoading"
            :file-list="[]"
            :max-count="20"
            multiple
            class="upload-zone"
          >
            <p class="upload-icon"><UploadOutlined /></p>
            <p class="upload-title">选择文件或拖放到此处</p>
            <p class="upload-hint">支持单选、多选；选择后立即解析</p>
          </a-upload-dragger>

          <a-spin :spinning="uploadLoading" tip="正在提取 Markdown 并生成批次名称">
            <section v-if="ingestItems.length" class="preview-section" aria-labelledby="preview-heading">
              <div class="preview-heading-row">
                <div>
                  <h2 id="preview-heading">导入预览</h2>
                  <span>{{ ingestItems.length }} 个文件已完成解析</span>
                </div>
                <a-tag color="success"><CheckOutlined /> 自动处理完成</a-tag>
              </div>

              <a-table
                class="desktop-preview-table"
                :columns="tableColumns"
                :data-source="ingestItems"
                :pagination="false"
                :row-key="ingestRowKey"
                :scroll="{ x: 1014 }"
                size="middle"
              >
                <template #bodyCell="{ column, record }">
                  <template v-if="column.key === 'file'">
                    <div class="file-cell">
                      <FileTextOutlined />
                      <div>
                        <strong>{{ record.filename }}</strong>
                        <span>{{ formatSize(record.size) }} · {{ record.extraction_method }}</span>
                      </div>
                    </div>
                  </template>
                  <template v-else-if="column.key === 'markdown'">
                    <button class="markdown-preview" type="button" @click="showMarkdown(record)">
                      <span>{{ record.markdown_preview }}</span>
                      <small><EyeOutlined /> 查看 Markdown</small>
                    </button>
                  </template>
                  <template v-else-if="column.key === 'batch'">
                    <a-form-item class="batch-field" :validate-status="record.batch_name.trim() ? '' : 'error'">
                      <a-input v-model:value="record.batch_name" :maxlength="120" aria-label="批次名称" />
                    </a-form-item>
                  </template>
                  <template v-else-if="column.key === 'actions'">
                    <a-tooltip title="移除">
                      <a-button type="text" danger shape="circle" aria-label="移除文件" @click="removeIngestItem(record.id)">
                        <DeleteOutlined />
                      </a-button>
                    </a-tooltip>
                  </template>
                </template>
              </a-table>

              <a-list class="mobile-preview-list" :data-source="ingestItems" :split="true">
                <template #renderItem="{ item }">
                  <a-list-item>
                    <div class="mobile-item-head">
                      <div class="file-cell">
                        <FileTextOutlined />
                        <div>
                          <strong>{{ item.filename }}</strong>
                          <span>{{ formatSize(item.size) }} · {{ item.extraction_method }}</span>
                        </div>
                      </div>
                      <a-tooltip title="移除">
                        <a-button type="text" danger shape="circle" aria-label="移除文件" @click="removeIngestItem(item.id)">
                          <DeleteOutlined />
                        </a-button>
                      </a-tooltip>
                    </div>
                    <button class="markdown-preview mobile-markdown" type="button" @click="showMarkdown(item)">
                      <span>{{ item.markdown_preview }}</span>
                      <small><EyeOutlined /> 查看 Markdown</small>
                    </button>
                    <label class="mobile-batch-label">
                      <span>批次名称</span>
                      <a-input v-model:value="item.batch_name" :maxlength="120" aria-label="批次名称" />
                    </label>
                  </a-list-item>
                </template>
              </a-list>

              <div class="confirm-bar">
                <span>请复核批次名称，确认后将一次性写入知识库。</span>
                <a-button type="primary" size="large" :disabled="!canCommitIngest" :loading="commitLoading" @click="commitIngest">
                  <CheckOutlined />确认批量入库
                </a-button>
              </div>
            </section>
            <a-empty v-else-if="!uploadLoading" class="empty-state" :image="false" description="尚未选择文件">
              <template #image><InboxOutlined /></template>
            </a-empty>
          </a-spin>
        </div>
      </a-tab-pane>

      <a-tab-pane key="qa" tab="问答沉淀">
        <a-form layout="vertical" class="secondary-form">
          <a-form-item label="问题" required><a-textarea v-model:value="qa.question" :rows="2" /></a-form-item>
          <a-form-item label="回答" required><a-textarea v-model:value="qa.answer" :rows="5" /></a-form-item>
          <a-row :gutter="12">
            <a-col :xs="24" :md="12"><a-form-item label="标题"><a-input v-model:value="qa.title" /></a-form-item></a-col>
            <a-col :xs="24" :md="12"><a-form-item label="Slug"><a-input v-model:value="qa.slug" placeholder="revenue-repurchase-qa" /></a-form-item></a-col>
          </a-row>
          <a-form-item label="标签"><a-input v-model:value="qa.tags" /></a-form-item>
          <a-form-item label="关联页面"><a-input v-model:value="qa.related" /></a-form-item>
          <a-space>
            <a-button type="primary" :loading="actionLoading" @click="createPreview"><EyeOutlined />生成预览</a-button>
            <a-button v-if="preview" type="primary" danger :loading="actionLoading" @click="commitPreview"><CheckOutlined />确认写入</a-button>
          </a-space>
        </a-form>
      </a-tab-pane>

      <a-tab-pane key="review" tab="页面复核">
        <div class="secondary-form">
          <a-steps class="review-steps" size="small" :current="reviewStep - 1">
            <a-step title="选择待复核页面" description="先确定要阅读的知识页" />
            <a-step title="阅读并完成复核" description="查看正文和来源后确认" />
          </a-steps>

          <template v-if="reviewStep === 1">
            <a-alert type="warning" show-icon message="确认后页面会进入答疑主检索集" />
            <a-button class="load-button" :loading="actionLoading" @click="loadPendingReviews">加载待复核页面</a-button>
            <a-empty v-if="!pendingReviews.length" description="尚未加载或没有待复核页面" />
            <a-radio-group v-else v-model:value="selectedReview" class="review-list" @change="handleReviewChange">
              <a-radio v-for="item in pendingReviews" :key="item.path" :value="item.path">
                <span class="review-row">
                  <span class="review-row-copy"><strong>{{ item.title }}</strong><small>{{ item.page_role }} · {{ item.maturity }} · {{ item.raw_path || '未登记本地来源' }}</small></span>
                  <a-button type="link" size="small" @click.stop="selectReview(item)"><EyeOutlined />查看详情</a-button>
                </span>
              </a-radio>
            </a-radio-group>
            <div v-if="selectedReview" class="review-selection-bar">
              <span v-if="reviewConfirmed" class="review-complete-state"><CheckOutlined /> 已完成正文复核，可以生成写入预览。</span>
              <span v-else>请点击条目右侧“查看详情”，阅读完成后再继续。</span>
              <a-space>
                <a-button type="primary" :disabled="!reviewConfirmed" :loading="actionLoading" @click="createPreview"><EyeOutlined />生成预览</a-button>
                <a-button v-if="preview" type="primary" danger :loading="actionLoading" @click="commitPreview"><CheckOutlined />确认复核</a-button>
              </a-space>
            </div>
          </template>

          <section v-else class="review-reader-panel" aria-labelledby="review-reader-title">
            <div class="review-reader-topbar">
              <a-button type="text" @click="reviewStep = 1"><ArrowLeftOutlined />返回页面列表</a-button>
              <a-tag v-if="reviewDetailComplete" color="blue">正文已加载</a-tag>
            </div>
            <a-spin :spinning="reviewDetailLoading" tip="正在读取页面正文">
              <template v-if="selectedReviewDetail">
                <header class="review-reader-header">
                  <h2 id="review-reader-title">{{ selectedReviewDetail.title }}</h2>
                  <p class="review-source">来源：{{ selectedReviewDetail.raw_path || '未登记本地来源' }} · {{ selectedReviewDetail.path }}</p>
                </header>
                <pre class="review-reader-body">{{ selectedReviewDetail.body }}</pre>
              </template>
              <a-empty v-else description="正在准备页面预览" />
            </a-spin>
            <a-alert v-if="!reviewDetailLoading && !reviewDetailComplete" class="review-reader-error" type="error" show-icon message="正文未完整加载，暂不能完成复核" />
            <div class="review-reader-footer">
              <span>请完整阅读正文、来源及页面内容，确认无误后完成复核。</span>
              <a-button type="primary" size="large" :disabled="!reviewDetailComplete || reviewDetailLoading" @click="completeReview"><CheckOutlined />完成复核</a-button>
            </div>
          </section>
        </div>
      </a-tab-pane>
    </a-tabs>

    <a-alert v-if="error" class="space" type="error" show-icon :message="error" closable @close="error = ''" />
    <a-card v-if="preview" class="space output-card" title="写入预览">
      <pre>{{ preview.output }}</pre>
      <template v-if="preview.review">
        <h3>复核正文</h3>
        <pre>{{ preview.review.body }}</pre>
        <p>来源：{{ preview.review.raw_path || '未登记本地来源' }}</p>
      </template>
    </a-card>
    <a-result v-if="result" class="space result-panel" status="success" title="维护任务已完成" :sub-title="resultSubtitle">
      <template #extra><a-button @click="result = null"><InboxOutlined />继续维护</a-button></template>
      <pre>{{ result.output }}</pre>
    </a-result>

    <a-modal v-model:open="markdownOpen" :title="markdownTitle" width="min(900px, 92vw)" :footer="null">
      <a-spin :spinning="markdownLoading">
        <div class="modal-title"><FileMarkdownOutlined /> Markdown 正文</div>
        <pre class="markdown-full">{{ markdownContent }}</pre>
      </a-spin>
    </a-modal>
  </section>
</template>

<style scoped>
.maintenance-page { width: min(1180px, 100%); }
.page-header { display: flex; align-items: flex-end; justify-content: space-between; gap: 24px; margin-bottom: 18px; }
.page-header .page-heading { margin-bottom: 6px; }
.page-header .page-subheading { margin: 0; }
.token-input { width: 260px; }
.maintenance-tabs { background: var(--app-surface); border: 1px solid var(--app-border); border-radius: 8px; box-shadow: var(--app-shadow); }
.maintenance-tabs :deep(.ant-tabs-nav) { margin: 0; padding: 0 24px; }
.maintenance-tabs :deep(.ant-tabs-content-holder) { border-top: 1px solid var(--app-border); }
.ingest-workspace { padding: 24px; }
.upload-zone :deep(.ant-upload-drag) { min-height: 174px; border-color: var(--app-border); border-radius: 8px; background: var(--app-bg); }
.upload-zone :deep(.ant-upload-drag:hover) { border-color: var(--app-accent); background: var(--app-accent-soft); }
.upload-icon { margin: 0 0 8px; color: var(--app-accent); font-size: 30px; }
.upload-title { margin: 0; color: var(--app-text); font-size: 16px; font-weight: 650; }
.upload-hint { margin: 6px 0 0; color: var(--app-muted); font-size: 12px; }
.preview-section { margin-top: 24px; }
.preview-heading-row { display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 12px; }
.preview-heading-row h2 { margin: 0 0 3px; font-size: 17px; }
.preview-heading-row span { color: var(--app-muted); font-size: 12px; }
.file-cell { display: flex; align-items: flex-start; gap: 10px; min-width: 0; }
.file-cell > :deep(.anticon) { flex: none; margin-top: 3px; color: var(--app-accent); font-size: 18px; }
.file-cell div { min-width: 0; }
.file-cell strong, .file-cell span { display: block; overflow-wrap: anywhere; }
.file-cell span { margin-top: 5px; color: var(--app-muted); font-size: 11px; }
.markdown-preview { display: block; width: 100%; padding: 0; color: inherit; background: transparent; border: 0; text-align: left; cursor: pointer; }
.markdown-preview > span { display: -webkit-box; max-height: 68px; overflow: hidden; color: var(--app-muted); font-family: Consolas, monospace; font-size: 12px; line-height: 1.45; white-space: pre-wrap; -webkit-box-orient: vertical; -webkit-line-clamp: 3; }
.markdown-preview small { display: block; margin-top: 7px; color: var(--app-accent); }
.batch-field { margin: 0; }
.mobile-preview-list { display: none; }
.confirm-bar { display: flex; align-items: center; justify-content: flex-end; gap: 20px; padding-top: 20px; }
.confirm-bar span { color: var(--app-muted); font-size: 12px; }
.empty-state { padding: 34px 0 8px; }
.empty-state :deep(.ant-empty-image) { height: auto; color: var(--app-subtle); font-size: 30px; }
.secondary-form { padding: 24px; }
.space { margin-top: 20px; }
.review-steps { margin-bottom: 24px; }
.load-button { margin: 14px 0; }
.review-list { display: grid; gap: 12px; margin: 8px 0 18px; }
.review-list :deep(.ant-radio-wrapper) { display: grid; grid-template-columns: 20px 1fr; align-items: start; }
.review-row { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; min-width: 0; }
.review-row-copy { display: block; min-width: 0; }
.review-row-copy strong, .review-row-copy small { display: block; overflow-wrap: anywhere; }
.review-row-copy small { margin-top: 4px; color: var(--app-muted); font-size: 12px; }
.review-row :deep(.ant-btn) { flex: none; margin-top: -6px; padding-inline: 4px; }
.review-selection-bar { display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-top: 20px; padding-top: 18px; border-top: 1px solid var(--app-border); }
.review-selection-bar > span { color: var(--app-muted); font-size: 12px; }
.review-complete-state { color: var(--app-success, #237b4b) !important; }
.review-source { color: var(--app-muted); font-size: 12px; overflow-wrap: anywhere; }
.review-reader-panel { margin-top: 4px; padding: 16px; border: 1px solid var(--app-border); border-radius: 8px; background: var(--app-surface); box-shadow: var(--app-shadow); }
.review-reader-topbar { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 14px; }
.review-reader-header { padding: 6px 4px 14px; border-bottom: 1px solid var(--app-border); }
.review-reader-header h2 { margin: 0 0 7px; font-size: 22px; }
.review-reader-body { max-height: min(62vh, 660px); min-height: 360px; margin: 0; overflow: auto; padding: 22px; background: var(--app-bg); border: 0; border-radius: 6px; color: var(--app-text); font-family: Consolas, 'Microsoft YaHei', monospace; font-size: 14px; line-height: 1.8; white-space: pre-wrap; word-break: break-word; }
.review-reader-error { margin-top: 14px; }
.review-reader-footer { display: flex; align-items: center; justify-content: space-between; gap: 18px; padding-top: 16px; }
.review-reader-footer > span { color: var(--app-muted); font-size: 12px; }
.output-card, .result-panel { box-shadow: var(--app-shadow); }
pre { max-height: 320px; overflow: auto; padding: 14px; background: var(--app-bg); border: 1px solid var(--app-border); border-radius: 6px; white-space: pre-wrap; word-break: break-word; }
.modal-title { margin-bottom: 10px; color: var(--app-muted); font-size: 12px; }
.markdown-full { max-height: 62vh; margin: 0; }
@media (max-width: 700px) {
  .maintenance-page { width: calc(100vw - 72px); max-width: calc(100vw - 72px); min-width: 0; overflow: hidden; }
  .page-header { align-items: stretch; flex-direction: column; gap: 12px; }
  .token-input { width: 100%; }
  .maintenance-tabs { min-width: 0; overflow: hidden; }
  .maintenance-tabs :deep(.ant-tabs-nav) { padding: 0 14px; }
  .ingest-workspace, .secondary-form { padding: 16px; }
  .desktop-preview-table { display: none; }
  .mobile-preview-list { display: block; border-top: 1px solid var(--app-border); }
  .mobile-preview-list :deep(.ant-list-item) { display: block; padding: 18px 0; }
  .mobile-item-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 10px; }
  .mobile-item-head .file-cell { min-width: 0; }
  .mobile-markdown { margin-top: 14px; padding: 10px; background: var(--app-bg); border: 1px solid var(--app-border); border-radius: 6px; }
  .mobile-batch-label { display: block; margin-top: 14px; }
  .mobile-batch-label > span { display: block; margin-bottom: 6px; color: var(--app-muted); font-size: 12px; }
  .confirm-bar { align-items: stretch; flex-direction: column; }
  .confirm-bar .ant-btn { width: 100%; }
  .review-selection-bar, .review-reader-footer { align-items: stretch; flex-direction: column; }
  .review-selection-bar .ant-space, .review-reader-footer .ant-btn { width: 100%; }
  .review-selection-bar .ant-space .ant-btn { flex: 1; }
  .review-reader-panel { padding: 12px; }
  .review-reader-body { min-height: 52vh; max-height: 58vh; padding: 16px; font-size: 13px; }
}
</style>
