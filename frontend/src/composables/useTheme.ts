import { computed, ref } from 'vue'

const saved = localStorage.getItem('cpa-zh-theme')
const dark = ref(saved === 'dark')
document.documentElement.dataset.theme = dark.value ? 'dark' : ''

export function useTheme() {
  const label = computed(() => (dark.value ? '浅色模式' : '深色模式'))
  function toggle() {
    dark.value = !dark.value
    document.documentElement.dataset.theme = dark.value ? 'dark' : ''
    localStorage.setItem('cpa-zh-theme', dark.value ? 'dark' : 'light')
  }
  return { dark, label, toggle }
}
