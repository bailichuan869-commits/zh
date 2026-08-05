import { computed, ref } from 'vue'

const saved = localStorage.getItem('cpa-zh-theme')
const prefersDark = window.matchMedia?.('(prefers-color-scheme: dark)').matches ?? false
const dark = ref(saved ? saved === 'dark' : prefersDark)

function applyTheme() {
  document.documentElement.dataset.theme = dark.value ? 'dark' : 'light'
  document.documentElement.style.colorScheme = dark.value ? 'dark' : 'light'
}

applyTheme()

export function useTheme() {
  const label = computed(() => (dark.value ? '浅色模式' : '深色模式'))

  function setTheme(nextDark: boolean) {
    dark.value = nextDark
    applyTheme()
    localStorage.setItem('cpa-zh-theme', dark.value ? 'dark' : 'light')
  }

  function toggle() {
    setTheme(!dark.value)
  }

  return { dark, label, setTheme, toggle }
}
