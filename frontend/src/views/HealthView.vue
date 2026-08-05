<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { CheckCircleOutlined, DatabaseOutlined, LinkOutlined, ReloadOutlined } from '@ant-design/icons-vue'
import { api, type Health } from '@/services/api'

const health = ref<Health | null>(null)
const loading = ref(true)
const error = ref('')
const healthy = computed(() => health.value?.status === 'ok' && health.value.index_ready)

async function load() {
  loading.value = true
  error.value = ''
  try {
    health.value = await api.health()
  } catch (reason) {
    error.value = reason instanceof Error ? reason.message : '无法读取知识库状态'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <section class="health-page">
    <header class="page-header">
      <div><p class="page-kicker">只读检查</p><h1 class="page-heading">知识库状态</h1><p class="page-subheading">索引、知识页面和关联关系的当前可用性。</p></div>
      <a-button :loading="loading" @click="load"><ReloadOutlined />刷新</a-button>
    </header>

    <a-alert v-if="error" type="error" show-icon :message="error">
      <template #action><a-button size="small" @click="load">重试</a-button></template>
    </a-alert>

    <a-spin :spinning="loading">
      <section v-if="health" class="health-status" :class="{ healthy }" aria-live="polite">
        <span class="health-status-icon"><CheckCircleOutlined /></span>
        <div>
          <strong>{{ healthy ? '知识库读取服务正常' : '知识库需要维护' }}</strong>
          <p>{{ healthy ? '搜索索引已就绪，Web 阅读入口可正常使用。' : '索引尚未就绪，请通过 Agent 或 tools/kb.py 执行维护。' }}</p>
        </div>
      </section>

      <div v-if="health" class="metric-grid">
        <div class="metric"><DatabaseOutlined /><span>检索索引</span><strong>{{ health.index_ready ? '已就绪' : '未就绪' }}</strong></div>
        <div class="metric"><CheckCircleOutlined /><span>知识页面</span><strong>{{ health.wiki_pages }}</strong></div>
        <div class="metric"><LinkOutlined /><span>关联目标</span><strong>{{ health.backlink_targets }}</strong></div>
      </div>
      <a-empty v-else-if="!loading && !error" description="暂无状态数据" />
    </a-spin>
  </section>
</template>

<style scoped>
.health-page {
  width: min(980px, 100%);
  padding: 38px 42px 70px;
}

.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 26px;
}

.health-status {
  min-height: 96px;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 20px;
  margin-top: 22px;
  background: var(--app-warning-soft);
  border: 1px solid color-mix(in srgb, var(--app-warning) 30%, var(--app-border));
  border-radius: 8px;
}

.health-status.healthy {
  background: var(--app-success-soft);
  border-color: color-mix(in srgb, var(--app-success) 28%, var(--app-border));
}

.health-status-icon {
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  flex: 0 0 34px;
  color: var(--app-success);
  background: var(--app-surface);
  border-radius: 50%;
}

.health-status-icon :deep(.anticon) {
  font-size: var(--app-icon-size);
}

.health-status strong {
  color: var(--app-text);
  font-weight: 500;
}

.health-status p {
  margin: 4px 0 0;
  color: var(--app-muted);
  font-size: 13px;
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  margin-top: 22px;
  border-top: 1px solid var(--app-border);
  border-bottom: 1px solid var(--app-border);
}

.metric {
  min-width: 0;
  display: grid;
  grid-template-columns: 22px minmax(0, 1fr);
  grid-template-rows: auto auto;
  gap: 5px 8px;
  padding: 18px 16px;
  border-right: 1px solid var(--app-border);
}

.metric:last-child {
  border-right: 0;
}

.metric > :deep(.anticon) {
  grid-row: 1 / 3;
  margin-top: 2px;
  color: var(--app-muted);
  font-size: var(--app-icon-size);
}

.metric span {
  color: var(--app-muted);
  font-size: 12px;
}

.metric strong {
  color: var(--app-text);
  font-size: 18px;
  font-weight: 500;
}

@media (max-width: 700px) {
  .health-page {
    width: 100%;
    padding: 28px 16px 50px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .metric-grid {
    grid-template-columns: 1fr;
  }

  .metric {
    border-right: 0;
    border-bottom: 1px solid var(--app-border);
  }

  .metric:last-child {
    border-bottom: 0;
  }
}
</style>
