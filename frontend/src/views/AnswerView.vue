<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { LinkOutlined, SendOutlined } from '@ant-design/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import { api, type AnswerCitation, type AnswerResult } from '@/services/api'

const router = useRouter()
const route = useRoute()
const question = ref('')
const topic = ref('')
const profile = ref('answer-current')
const asOf = ref('')
const depth = ref('standard')
const loading = ref(false)
const error = ref('')
const result = ref<AnswerResult | null>(null)
const lastAutoSubmittedQuestion = ref('')
const topics = [
  { value: 'revenue-recognition', label: '收入确认' },
  { value: 'leases', label: '租赁' },
  { value: 'financial-instruments', label: '金融工具' },
  { value: 'consolidation', label: '合并范围与控制' },
  { value: 'cash-flow', label: '现金流量表与列报' },
]
const profiles = [
  { value: 'answer-current', label: '当前有效答疑证据' },
  { value: 'case-review', label: '案例复核资料' },
  { value: 'learning', label: '学习对照资料' },
]
const hasResult = computed(() => result.value !== null)

async function ask() {
  if (!question.value.trim()) return
  loading.value = true; error.value = ''; result.value = null
  try { result.value = await api.answer(question.value.trim(), topic.value, { profile: profile.value, as_of: asOf.value, depth: depth.value }) } catch (reason) { error.value = reason instanceof Error ? reason.message : '答疑服务暂时不可用' } finally { loading.value = false }
}
watch(() => String(route.query.question ?? '').trim(), value => {
  if (!value || value === lastAutoSubmittedQuestion.value) return
  question.value = value
  lastAutoSubmittedQuestion.value = value
  ask()
}, { immediate: true })
function openCitation(item: AnswerCitation) {
  router.push({
    path: item.path.startsWith('wiki/') ? '/document' : '/raw',
    query: { path: item.path },
    ...(item.section_anchor ? { hash: `#${item.section_anchor}` } : {}),
  })
}
</script>

<template>
  <section class="answer-page">
    <header><h1 class="page-heading">知识答疑</h1><p class="page-subheading">回答仅依据已复核知识页、案例卡与权威原文，并保留每项证据入口。</p></header>
    <a-card :bordered="false" class="question-card">
      <a-form layout="vertical" @finish="ask"><a-form-item label="问题"><a-textarea v-model:value="question" :rows="4" placeholder="例如：含可变付款的售后租回应如何判断？" /></a-form-item><div class="answer-controls"><a-form-item label="主题范围"><a-select v-model:value="topic" allow-clear placeholder="自动从全部已复核主题中检索"><a-select-option v-for="item in topics" :key="item.value" :value="item.value">{{ item.label }}</a-select-option></a-select></a-form-item><a-form-item label="证据范围"><a-select v-model:value="profile"><a-select-option v-for="item in profiles" :key="item.value" :value="item.value">{{ item.label }}</a-select-option></a-select></a-form-item><a-form-item label="截至日期"><a-input v-model:value="asOf" type="date" /></a-form-item><a-form-item label="检索深度"><a-radio-group v-model:value="depth" button-style="solid"><a-radio-button value="standard">标准</a-radio-button><a-radio-button value="deep">深入</a-radio-button></a-radio-group></a-form-item></div><a-button type="primary" html-type="submit" :loading="loading"><SendOutlined />获取有依据的答复</a-button></a-form>
    </a-card>
    <a-alert v-if="error" class="space" type="error" show-icon :message="error" />
    <a-spin :spinning="loading"><section v-if="hasResult" class="space"><a-alert v-if="result?.insufficient_evidence" type="warning" show-icon message="现有已复核资料不足" description="系统未生成专业结论；请先核验下方资料或补充复核知识页。" /><a-alert v-if="result?.risk_flags.length" type="info" show-icon message="证据链提示" :description="result?.risk_flags.join('；')" /><a-card v-if="!result?.insufficient_evidence" :bordered="false" class="answer-card"><template #title>答复</template><div class="answer-text">{{ result?.answer }}</div><a-tag color="blue">{{ result?.confidence }}</a-tag></a-card><a-card :bordered="false" class="citations-card" title="证据与原文"><a-empty v-if="!result?.citations.length" description="未找到可展示的相关资料" /><a-list v-else :data-source="result?.citations"><template #renderItem="{ item }"><a-list-item><a-list-item-meta :title="item.title" :description="item.excerpt" /><template #actions><a @click="openCitation(item)"><LinkOutlined />打开</a><a v-if="item.source_url" :href="item.source_url" target="_blank" rel="noreferrer">来源</a></template><div class="citation-meta"><a-tag v-if="item.answer_ready" color="green">已复核</a-tag><a-tag v-if="item.authority">{{ item.authority }}</a-tag><a-tag v-if="item.section">章节：{{ item.section }}</a-tag><a-tag v-if="item.version">版本：{{ item.version }}</a-tag><a-tag v-if="item.lifecycle_status">状态：{{ item.lifecycle_status }}</a-tag><span v-if="item.effective_from || item.effective_to">生效：{{ item.effective_from || '未声明' }} 至 {{ item.effective_to || '未声明' }}</span></div></a-list-item></template></a-list></a-card></section></a-spin>
  </section>
</template>

<style scoped>.answer-page { max-width: 1050px; }.question-card, .answer-card, .citations-card { box-shadow: var(--app-shadow); }.question-card :deep(.ant-card-body) { padding: 24px; }.space { margin-top: 22px; }.answer-text { margin-bottom: 18px; white-space: pre-wrap; line-height: 1.8; }.citations-card { margin-top: 16px; }.citations-card :deep(.ant-list-item-meta-description) { line-height: 1.65; }.answer-controls { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 16px; }.citation-meta { display: flex; align-items: center; flex-wrap: wrap; gap: 6px; margin-top: 10px; color: var(--app-muted); font-size: 12px; }.citation-meta span { overflow-wrap: anywhere; } @media (max-width: 680px) { .answer-controls { grid-template-columns: 1fr; } }</style>
