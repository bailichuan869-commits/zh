<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MarkdownArticle from '@/components/MarkdownArticle.vue'
import { api, type Document } from '@/services/api'
const route = useRoute(); const router = useRouter(); const document = ref<Document | null>(null); const loading = ref(false); const error = ref('')
const path = computed(() => String(route.query.path ?? ''))
async function load() { if (!path.value) return; loading.value = true; error.value = ''; try { document.value = await api.document(path.value) } catch (reason) { error.value = reason instanceof Error ? reason.message : '无法读取页面' } finally { loading.value = false } }
watch(path, load, { immediate: true })
function openBacklink(target: string) { router.push({ path: '/document', query: { path: `wiki/${target}.md` } }) }
</script>
<template><a-spin :spinning="loading"><a-alert v-if="error" type="error" :message="error" show-icon /><template v-else-if="document"><a-page-header :title="document.frontmatter.title || document.path" :sub-title="document.path" @back="router.back()"><template #tags><a-tag v-if="document.frontmatter.type">{{ document.frontmatter.type }}</a-tag><a-tag v-if="document.frontmatter.maturity">{{ document.frontmatter.maturity }}</a-tag></template></a-page-header><a-row :gutter="24"><a-col :xs="24" :lg="18"><a-card><MarkdownArticle :source="document.markdown" /></a-card></a-col><a-col :xs="24" :lg="6"><a-card title="反向链接"><a-empty v-if="!document.backlinks.length" description="暂无反向链接" /><a-list v-else size="small" :data-source="document.backlinks"><template #renderItem="{ item }"><a-list-item><a @click="openBacklink(item.path)">{{ item.title }}</a></a-list-item></template></a-list></a-card></a-col></a-row></template></a-spin></template>
