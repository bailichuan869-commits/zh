<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { FileTextOutlined, FolderOpenOutlined, LinkOutlined, SearchOutlined } from '@ant-design/icons-vue'
import { api, type Summary } from '@/services/api'
const summary = ref<Summary | null>(null)
const loading = ref(true)
const error = ref('')
onMounted(async () => { try { summary.value = await api.summary() } catch (reason) { error.value = reason instanceof Error ? reason.message : '无法读取知识库统计' } finally { loading.value = false } })
</script>
<template>
  <section class="intro"><div><h1>CPA-ZH 知识库</h1><p>面向中国注册会计师行业的法规、准则、政策与审计实务工作台。</p></div><router-link to="/search"><a-button type="primary" size="large"><SearchOutlined />开始检索</a-button></router-link></section>
  <a-alert v-if="error" type="error" :message="error" show-icon />
  <a-spin :spinning="loading"><a-row :gutter="16" class="stats"><a-col :xs="12" :md="6"><a-card><FileTextOutlined /><strong>{{ summary?.total ?? '-' }}</strong><span>已索引资料</span></a-card></a-col><a-col :xs="12" :md="6"><a-card><FolderOpenOutlined /><strong>{{ summary?.wiki_pages ?? '-' }}</strong><span>知识页面</span></a-card></a-col><a-col :xs="12" :md="6"><a-card><LinkOutlined /><strong>{{ summary?.backlink_targets ?? '-' }}</strong><span>反链目标</span></a-card></a-col><a-col :xs="12" :md="6"><a-card><FileTextOutlined /><strong>{{ summary?.answer_ready ?? '-' }}</strong><span>已复核问答页</span></a-card></a-col></a-row></a-spin>
  <a-card title="浏览方式" class="guide"><a-space direction="vertical"><router-link to="/search">全文检索与领域筛选</router-link><span>知识页面提供 Markdown 正文、元数据与反向链接。</span><span>原始资料保持只读；入库、索引与质量检查继续使用 Python 命令行。</span></a-space></a-card>
</template>
<style scoped>
.intro { display: flex; align-items: center; justify-content: space-between; gap: 24px; margin: 20px 0 32px; }.intro h1 { margin: 0; font-size: 28px; }.intro p { color: var(--app-muted); margin: 8px 0 0; }.stats { margin-bottom: 24px; }.stats :deep(.ant-card-body) { display: grid; gap: 6px; }.stats strong { font-size: 28px; }.stats span { color: var(--app-muted); }.guide { max-width: 760px; } @media(max-width: 680px){.intro { align-items: flex-start; flex-direction: column; }}
</style>
