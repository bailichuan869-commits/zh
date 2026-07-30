<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '@/services/api'
const route = useRoute(); const path = computed(() => String(route.query.path ?? '')); const url = computed(() => api.rawUrl(path.value)); const isHtml = computed(() => /\.html?$/i.test(path.value))
</script>
<template><a-space direction="vertical" size="large" style="width:100%"><a-page-header title="原始资料" :sub-title="path" /><a-alert v-if="!path" type="warning" message="请选择要查看的原始资料" /><template v-else><a :href="url" target="_blank" rel="noopener"><a-button>在新窗口打开或下载</a-button></a><iframe v-if="isHtml" class="preview" :src="url" title="原始 HTML 预览" sandbox="allow-same-origin" /><a-card v-else><p>该文件由后端受限提供。使用上方按钮可在浏览器中预览或下载。</p></a-card></template></a-space></template>
<style scoped>.preview { width: 100%; min-height: 70vh; border: 1px solid var(--app-border); }</style>
