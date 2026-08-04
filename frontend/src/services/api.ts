export interface SearchResult { kind: string; title: string; path: string; source_url: string; domain: string; topic: string; snippet: string; page_role: string; maturity: string; answer_ready: boolean }
export interface Summary { kinds: Record<string, number>; roles: Record<string, number>; maturity: Record<string, number>; answer_ready: number; total: number; wiki_pages: number; backlink_targets: number }
export interface Document { path: string; frontmatter: Record<string, string>; markdown: string; backlinks: Array<{ path: string; title: string }> }
export interface AnswerCitation { path: string; title: string; excerpt: string; source_url: string; maturity: string; authority: string; answer_ready: boolean }
export interface AnswerResult { answer: string; citations: AnswerCitation[]; confidence: string; insufficient_evidence: boolean }
export interface MaintenancePreview { preview_token: string; kind: string; output: string; expires_in: number; review?: { path: string; title: string; raw_path: string; body: string; changes: Record<string, string | boolean>; content_sha256: string } }
export interface MaintenanceResult { status: string; output: string; health: string }
export interface IngestUploadItem { id: string; filename: string; size: number; markdown_preview: string; markdown_length: number; preview_truncated: boolean; batch_name: string; extraction_method: string }
export interface IngestUploadPreview { session_token: string; items: IngestUploadItem[]; expires_in: number }
export interface PendingReview { path: string; title: string; page_role: string; maturity: string; raw_path: string; body_preview: string; content_sha256: string }
export interface AIConfiguration { provider: string; base_url: string; model: string; enabled: boolean; key_configured: boolean; simulated?: boolean }
export interface AIConnectionResult { status: string; message: string }

const base = import.meta.env.VITE_API_BASE_URL ?? ''
async function request<T>(url: string): Promise<T> {
  const response = await fetch(`${base}${url}`)
  if (!response.ok) throw new Error((await response.text()) || `请求失败 (${response.status})`)
  return response.json() as Promise<T>
}
async function write<T>(url: string, body: unknown, token: string): Promise<T> {
  const response = await fetch(`${base}${url}`, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }, body: JSON.stringify(body) })
  if (!response.ok) throw new Error((await response.text()) || `请求失败 (${response.status})`)
  return response.json() as Promise<T>
}
async function post<T>(url: string, body: unknown): Promise<T> {
  const response = await fetch(`${base}${url}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
  if (!response.ok) throw new Error((await response.text()) || `请求失败 (${response.status})`)
  return response.json() as Promise<T>
}
async function maintenanceRead<T>(url: string, token: string): Promise<T> {
  const response = await fetch(`${base}${url}`, { headers: { Authorization: `Bearer ${token}` } })
  if (!response.ok) throw new Error((await response.text()) || `请求失败 (${response.status})`)
  return response.json() as Promise<T>
}
async function upload<T>(url: string, files: File[], token: string): Promise<T> {
  const body = new FormData()
  files.forEach(file => body.append('files', file, file.name))
  const response = await fetch(`${base}${url}`, { method: 'POST', headers: { Authorization: `Bearer ${token}` }, body })
  if (!response.ok) throw new Error((await response.text()) || `请求失败 (${response.status})`)
  return response.json() as Promise<T>
}
export const api = {
  summary: () => request<Summary>('/api/v1/library/summary'),
  tree: () => request<unknown>('/api/v1/navigation/tree'),
  search: (q: string, domain = '', kind = '', offset = 0) => request<{ results: SearchResult[]; total: number; facets: [string, number][]; kinds: Record<string, number>; engine: string }>(`/api/v1/search?${new URLSearchParams({ q, domain, kind, limit: '30', offset: String(offset) })}`),
  document: (path: string) => request<Document>(`/api/v1/documents?${new URLSearchParams({ path })}`),
  rawUrl: (path: string) => `${base}/api/v1/files?${new URLSearchParams({ path })}`,
  answer: (question: string, topic = '') => post<AnswerResult>('/api/v1/answers', { question, topic }),
  previewQa: (body: Record<string, string>, token: string) => write<MaintenancePreview>('/maintenance/v1/qa/preview', body, token),
  commitQa: (body: Record<string, string>, previewToken: string, token: string) => write<MaintenanceResult>(`/maintenance/v1/qa/commit?${new URLSearchParams({ preview_token: previewToken })}`, body, token),
  previewIngest: (body: Record<string, string>, token: string) => write<MaintenancePreview>('/maintenance/v1/ingest/preview', body, token),
  commitIngest: (body: Record<string, string>, previewToken: string, token: string) => write<MaintenanceResult>(`/maintenance/v1/ingest/commit?${new URLSearchParams({ preview_token: previewToken })}`, body, token),
  uploadIngest: (files: File[], token: string) => upload<IngestUploadPreview>('/maintenance/v1/ingest/upload', files, token),
  uploadedMarkdown: (sessionToken: string, itemId: string, token: string) => maintenanceRead<{ markdown: string }>(`/maintenance/v1/ingest/${encodeURIComponent(sessionToken)}/items/${encodeURIComponent(itemId)}/markdown`, token),
  commitUploadedIngest: (sessionToken: string, items: Array<{ id: string; batch_name: string }>, token: string) => write<MaintenanceResult & { imported_count: number }>('/maintenance/v1/ingest/batch-commit', { session_token: sessionToken, items }, token),
  pendingReviews: (token: string) => maintenanceRead<{ items: PendingReview[] }>('/maintenance/v1/review/pending', token),
  previewReview: (path: string, contentSha256: string, confirmed: boolean, token: string) => write<MaintenancePreview>('/maintenance/v1/review/preview', { path, content_sha256: contentSha256, confirmed }, token),
  commitReview: (path: string, contentSha256: string, confirmed: boolean, previewToken: string, token: string) => write<MaintenanceResult>(`/maintenance/v1/review/commit?${new URLSearchParams({ preview_token: previewToken })}`, { path, content_sha256: contentSha256, confirmed }, token),
  aiConfig: (token: string) => maintenanceRead<AIConfiguration>('/maintenance/v1/ai-config', token),
  saveAiConfig: (body: Omit<AIConfiguration, 'key_configured' | 'simulated'> & { api_key: string }, token: string) => write<AIConfiguration>('/maintenance/v1/ai-config', body, token),
  testAiConfig: (token: string) => write<AIConnectionResult>('/maintenance/v1/ai-config/test', {}, token),
}
