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
  if (match) {
    event.preventDefault()
    router.push({ path: '/document', query: { path: `wiki/${match[1]}` } })
  }
}
</script>

<template><article class="markdown-article" @click="navigate" v-html="rendered" /></template>

<style scoped>
.markdown-article {
  color: var(--app-text);
  font-size: 16px;
  line-height: 1.9;
}

.markdown-article :deep(h1),
.markdown-article :deep(h2),
.markdown-article :deep(h3),
.markdown-article :deep(h4) {
  color: var(--app-text);
  line-height: 1.45;
  font-weight: 500;
  letter-spacing: 0;
}

.markdown-article :deep(h1) {
  margin: 1.8em 0 0.7em;
  font-size: 26px;
}

.markdown-article :deep(h2) {
  margin: 2em 0 0.7em;
  font-size: 22px;
}

.markdown-article :deep(h3) {
  margin: 1.7em 0 0.6em;
  font-size: 18px;
}

.markdown-article :deep(p) {
  margin: 0 0 1.15em;
}

.markdown-article :deep(ul),
.markdown-article :deep(ol) {
  padding-left: 1.5em;
  margin: 0 0 1.2em;
}

.markdown-article :deep(li) {
  margin: 0.3em 0;
}

.markdown-article :deep(a) {
  color: var(--app-accent);
  text-underline-offset: 3px;
}

.markdown-article :deep(blockquote) {
  margin: 1.6em 0;
  padding: 16px 18px;
  color: var(--app-text);
  background: var(--reader-quote);
  border-left: 3px solid var(--app-accent);
  border-radius: 0 6px 6px 0;
}

.markdown-article :deep(blockquote p:last-child) {
  margin-bottom: 0;
}

.markdown-article :deep(pre) {
  max-width: 100%;
  overflow: auto;
  padding: 16px;
  background: var(--reader-code);
  border: 1px solid var(--reader-rule);
  border-radius: 6px;
}

.markdown-article :deep(code) {
  font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
  font-size: 0.9em;
}

.markdown-article :deep(:not(pre) > code) {
  padding: 2px 5px;
  background: var(--app-code);
  border-radius: 4px;
}

.markdown-article :deep(table) {
  width: 100%;
  margin: 1.5em 0;
  border-collapse: collapse;
}

.markdown-article :deep(th),
.markdown-article :deep(td) {
  padding: 10px 12px;
  border-bottom: 1px solid var(--app-border);
  text-align: left;
  vertical-align: top;
  overflow-wrap: anywhere;
}

.markdown-article :deep(th) {
  color: var(--app-muted);
  font-size: 12px;
  font-weight: 500;
}

.markdown-article :deep(td code) {
  white-space: normal;
  overflow-wrap: anywhere;
}

.markdown-article :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 6px;
}

.markdown-article :deep(hr) {
  height: 1px;
  margin: 2em 0;
  background: var(--app-border);
  border: 0;
}

@media (max-width: 680px) {
  .markdown-article {
    font-size: 15px;
    line-height: 1.82;
  }
}
</style>
