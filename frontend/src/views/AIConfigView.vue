<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import { ApiOutlined, CheckCircleOutlined, CloudServerOutlined, SaveOutlined, SafetyCertificateOutlined } from '@ant-design/icons-vue'
import { api, type AIConfiguration, type AIConnectionResult } from '@/services/api'

const token = ref('')
const loading = ref(false)
const saving = ref(false)
const testing = ref(false)
const error = ref('')
const message = ref('')
const saved = ref<AIConfiguration | null>(null)
const form = reactive({ provider: 'openai-compatible', base_url: 'https://api.openai.com/v1', model: 'gpt-4.1-mini', enabled: false, api_key: '' })
const keyStatus = computed(() => saved.value?.key_configured ? '已配置' : '未配置')
const keyStatusColor = computed(() => saved.value?.key_configured ? 'success' : 'default')

function requireToken() { if (!token.value.trim()) { error.value = '请输入本机维护令牌'; return false }; return true }
function applyConfig(config: AIConfiguration) { saved.value = config; form.provider = config.provider; form.base_url = config.base_url; form.model = config.model; form.enabled = config.enabled; form.api_key = '' }
async function load() { if (!requireToken()) return; loading.value = true; error.value = ''; message.value = ''; try { applyConfig(await api.aiConfig(token.value.trim())) } catch (reason) { error.value = reason instanceof Error ? reason.message : '无法读取 AI 配置' } finally { loading.value = false } }
async function save() { if (!requireToken()) return; saving.value = true; error.value = ''; message.value = ''; try { const config = await api.saveAiConfig({ ...form }, token.value.trim()); applyConfig(config); message.value = config.simulated ? '开发模拟配置已验证，未保存到本机。' : 'AI 配置已保存到本机。' } catch (reason) { error.value = reason instanceof Error ? reason.message : '无法保存 AI 配置' } finally { saving.value = false } }
async function testConnection() { if (!requireToken()) return; testing.value = true; error.value = ''; message.value = ''; try { const result: AIConnectionResult = await api.testAiConfig(token.value.trim()); message.value = result.message } catch (reason) { error.value = reason instanceof Error ? reason.message : '模型服务连接失败' } finally { testing.value = false } }
</script>

<template>
  <section class="ai-config-page">
    <header class="page-header"><div><p class="eyebrow">AI SETTINGS</p><h1 class="page-heading">AI 配置</h1><p class="page-subheading">集中管理模型服务、连接地址与本机密钥，不会将密钥发送到浏览器存储或仓库。</p></div><a-tag :color="keyStatusColor"><SafetyCertificateOutlined /> 密钥{{ keyStatus }}</a-tag></header>
    <a-alert type="info" show-icon message="本机受控配置" description="保存与连通性测试均需维护令牌。API 密钥仅写入当前 Windows 用户的本机配置目录，页面只显示是否已配置。" />
    <a-row :gutter="[20, 20]" class="config-grid">
      <a-col :xs="24" :xl="16"><a-card :bordered="false" class="config-card"><template #title><span class="card-title"><ApiOutlined /> 模型服务</span></template><a-form layout="vertical" @finish="save"><a-form-item label="维护令牌" required><a-input-password v-model:value="token" autocomplete="off" placeholder="CPA_ZH_MAINTENANCE_TOKEN" /></a-form-item><a-form-item label="服务商"><a-select v-model:value="form.provider"><a-select-option value="openai-compatible">OpenAI 兼容服务</a-select-option><a-select-option value="openai">OpenAI</a-select-option><a-select-option value="deepseek">DeepSeek</a-select-option><a-select-option value="qwen">通义千问</a-select-option></a-select></a-form-item><a-form-item label="服务地址" required><a-input v-model:value="form.base_url" placeholder="https://api.openai.com/v1" /></a-form-item><a-form-item label="模型名称" required><a-input v-model:value="form.model" placeholder="gpt-4.1-mini" /></a-form-item><a-form-item label="API 密钥"><a-input-password v-model:value="form.api_key" autocomplete="new-password" :placeholder="saved?.key_configured ? '留空以保留当前密钥' : '输入 API 密钥'" /></a-form-item><a-form-item><a-switch v-model:checked="form.enabled" /><span class="switch-label">启用此模型配置</span></a-form-item><a-space><a-button type="primary" html-type="submit" :loading="saving"><SaveOutlined />保存配置</a-button><a-button :loading="testing" @click="testConnection"><CloudServerOutlined />测试连接</a-button><a-button :loading="loading" @click="load">读取当前配置</a-button></a-space></a-form></a-card></a-col>
      <a-col :xs="24" :xl="8"><aside class="status-stack"><a-card :bordered="false" class="status-card"><template #title><span class="card-title">当前状态</span></template><a-descriptions :column="1" size="small"><a-descriptions-item label="服务商">{{ saved?.provider || '未读取' }}</a-descriptions-item><a-descriptions-item label="模型">{{ saved?.model || '未读取' }}</a-descriptions-item><a-descriptions-item label="启用状态"><a-tag :color="saved?.enabled ? 'success' : 'default'">{{ saved?.enabled ? '已启用' : '未启用' }}</a-tag></a-descriptions-item><a-descriptions-item label="密钥"><a-tag :color="keyStatusColor">{{ keyStatus }}</a-tag></a-descriptions-item></a-descriptions></a-card><a-card :bordered="false" class="status-card"><template #title><span class="card-title">适配说明</span></template><p>支持 OpenAI Responses API 兼容服务。不同服务商通常只需填写对应的服务地址、模型名称和密钥。</p><p>未启用或未配置密钥时，答疑服务继续使用服务端环境变量。</p></a-card></aside></a-col>
    </a-row>
    <a-alert v-if="error" class="feedback" type="error" show-icon :message="error" /><a-alert v-if="message" class="feedback" type="success" show-icon :message="message"><template #icon><CheckCircleOutlined /></template></a-alert>
  </section>
</template>

<style scoped>
.ai-config-page { max-width: 1180px; }.page-header { display:flex; align-items:flex-start; justify-content:space-between; gap:20px; margin:14px 0 20px; }.eyebrow { margin:0 0 7px; color:#4b7edb; font-size:11px; font-weight:700; letter-spacing:1.2px; }.page-header :deep(.ant-tag) { margin:6px 0 0; padding:4px 9px; }.config-grid { margin-top:20px; }.config-card,.status-card { border:1px solid var(--app-border); box-shadow:var(--app-shadow); }.config-card :deep(.ant-card-body) { padding:24px; }.card-title { display:inline-flex; align-items:center; gap:8px; color:var(--app-text); font-weight:700; }.card-title :deep(.anticon) { color:var(--app-accent); }.switch-label { margin-left:10px; color:var(--app-text); }.status-stack { display:grid; gap:16px; }.status-card p { margin:0 0 12px; color:var(--app-muted); line-height:1.75; }.status-card p:last-child { margin-bottom:0; }.feedback { margin-top:20px; } @media(max-width:640px) { .page-header { flex-direction:column; }.config-card :deep(.ant-card-body) { padding:18px; } }
</style>
