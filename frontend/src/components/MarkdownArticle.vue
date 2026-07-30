<script setup lang="ts">
import DOMPurify from 'dompurify'
import MarkdownIt from 'markdown-it'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps<{ source: string }>()
const router = useRouter()
const parser = new MarkdownIt({ html: false, linkify: true, breaks: true })
const rendered = computed(() => DOMPurify.sanitize(parser.render(props.source)))
function navigate(event: MouseEvent) {
  const anchor = (event.target as HTMLElement).closest('a')
  if (!anchor?.href) return
  const match = anchor.getAttribute('href')?.match(/^wiki\/(.+\.md)$/)
  if (match) { event.preventDefault(); router.push({ path: '/document', query: { path: `wiki/${match[1]}` } }) }
}
</script>
<template><article class="markdown" @click="navigate" v-html="rendered" /></template>
<style scoped>
.markdown :deep(h1), .markdown :deep(h2), .markdown :deep(h3) { color: var(--app-text); margin-top: 1.6em; }
.markdown :deep(pre) { overflow: auto; padding: 14px; background: var(--app-code); border-radius: 6px; }
.markdown :deep(blockquote) { border-left: 3px solid var(--app-accent); margin: 1em 0; padding-left: 14px; color: var(--app-muted); }
.markdown :deep(img) { max-width: 100%; }
</style>
