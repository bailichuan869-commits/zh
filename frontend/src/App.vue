<script setup lang="ts">
import { computed } from 'vue'
import { ConfigProvider, theme as antTheme } from 'ant-design-vue'
import AppShell from '@/components/AppShell.vue'
import { useTheme } from '@/composables/useTheme'

const { dark } = useTheme()
const themeConfig = computed(() => ({
  algorithm: dark.value ? antTheme.darkAlgorithm : antTheme.defaultAlgorithm,
  token: {
    colorPrimary: dark.value ? '#7da8ff' : '#2765d9',
    colorSuccess: dark.value ? '#75c891' : '#2f7d4b',
    colorWarning: dark.value ? '#dfb85b' : '#936500',
    colorError: dark.value ? '#ef8d8d' : '#b84040',
    colorBgBase: dark.value ? '#20201f' : '#ffffff',
    colorTextBase: dark.value ? '#f0f0ec' : '#20201e',
    borderRadius: 6,
    controlHeight: 36,
    fontFamily: 'Inter, "Segoe UI", "Microsoft YaHei", "PingFang SC", system-ui, sans-serif',
  },
}))
</script>

<template>
  <ConfigProvider :theme="themeConfig">
    <AppShell><router-view /></AppShell>
  </ConfigProvider>
</template>
