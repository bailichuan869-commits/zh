export interface SearchResult { kind: string; title: string; path: string; source_url: string; domain: string; topic: string; snippet: string; page_role: string; maturity: string; answer_ready: boolean }
export interface Summary { kinds: Record<string, number>; roles: Record<string, number>; maturity: Record<string, number>; answer_ready: number; total: number; wiki_pages: number; backlink_targets: number }
export interface Document { path: string; frontmatter: Record<string, string>; markdown: string; backlinks: Array<{ path: string; title: string }> }

const base = import.meta.env.VITE_API_BASE_URL ?? ''
async function request<T>(url: string): Promise<T> {
  const response = await fetch(`${base}${url}`)
  if (!response.ok) throw new Error((await response.text()) || `请求失败 (${response.status})`)
  return response.json() as Promise<T>
}
export const api = {
  summary: () => request<Summary>('/api/v1/library/summary'),
  tree: () => request<unknown>('/api/v1/navigation/tree'),
  search: (q: string, domain = '', kind = '', offset = 0) => request<{ results: SearchResult[]; total: number; facets: [string, number][]; kinds: Record<string, number>; engine: string }>(`/api/v1/search?${new URLSearchParams({ q, domain, kind, limit: '30', offset: String(offset) })}`),
  document: (path: string) => request<Document>(`/api/v1/documents?${new URLSearchParams({ path })}`),
  rawUrl: (path: string) => `${base}/api/v1/files?${new URLSearchParams({ path })}`,
}
