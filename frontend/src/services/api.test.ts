import { afterEach, describe, expect, it, vi } from 'vitest'
import { api } from './api'

describe('knowledge API client', () => {
  afterEach(() => vi.unstubAllGlobals())

  it('uses the versioned search endpoint and encodes filters', async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({
      results: [], total: 0, facets: [], kinds: { wiki: 0, raw: 0 }, engine: 'like',
    }), { status: 200 }))
    vi.stubGlobal('fetch', fetchMock)

    await api.search('收入 确认', 'accounting', 'wiki', 30)

    expect(fetchMock).toHaveBeenCalledWith(
      '/api/v1/search?q=%E6%94%B6%E5%85%A5+%E7%A1%AE%E8%AE%A4&domain=accounting&kind=wiki&limit=30&offset=30',
    )
  })

  it('returns API failures with the response body', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response('service unavailable', { status: 503 })))

    await expect(api.summary()).rejects.toThrow('service unavailable')
  })

  it('constructs raw asset URLs through the versioned API', () => {
    expect(api.rawUrl('raw/laws/example.md')).toBe('/api/v1/files?path=raw%2Flaws%2Fexample.md')
  })

  it('reads raw markdown text through the restricted file endpoint', async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response('# 原始资料', { status: 200 }))
    vi.stubGlobal('fetch', fetchMock)

    await expect(api.rawText('raw/laws/example.md')).resolves.toBe('# 原始资料')
    expect(fetchMock).toHaveBeenCalledWith('/api/v1/files?path=raw%2Flaws%2Fexample.md')
  })

  it('reads the versioned knowledge-base health endpoint', async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ status: 'ok', index_ready: true, wiki_pages: 886, backlink_targets: 120 }), { status: 200 }))
    vi.stubGlobal('fetch', fetchMock)

    await api.health()

    expect(fetchMock).toHaveBeenCalledWith('/api/v1/health')
  })

  it('posts questions to the answer endpoint', async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ answer: '', citations: [], confidence: 'insufficient', insufficient_evidence: true }), { status: 200 }))
    vi.stubGlobal('fetch', fetchMock)

    await api.answer('收入确认要看什么')

    expect(fetchMock).toHaveBeenCalledWith('/api/v1/answers', expect.objectContaining({ method: 'POST' }))
  })

  it('sends AI configuration only to the protected maintenance API', async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ provider: 'openai-compatible', base_url: 'https://example.com/v1', model: 'demo', enabled: true, key_configured: true }), { status: 200 }))
    vi.stubGlobal('fetch', fetchMock)

    await api.saveAiConfig({ provider: 'openai-compatible', base_url: 'https://example.com/v1', model: 'demo', enabled: true, api_key: 'secret' }, 'maintenance-token')

    expect(fetchMock).toHaveBeenCalledWith('/maintenance/v1/ai-config', expect.objectContaining({ method: 'POST', headers: expect.objectContaining({ Authorization: 'Bearer maintenance-token' }) }))
  })

  it('uploads one or more files as protected multipart data', async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ session_token: 'session', items: [], expires_in: 1800 }), { status: 200 }))
    vi.stubGlobal('fetch', fetchMock)
    const file = new File(['# 收入确认'], 'case.md', { type: 'text/markdown' })

    await api.uploadIngest([file], 'maintenance-token')

    const [, options] = fetchMock.mock.calls[0]
    expect(options.headers).toEqual({ Authorization: 'Bearer maintenance-token' })
    expect(options.body).toBeInstanceOf(FormData)
    expect(options.body.getAll('files')).toHaveLength(1)
  })

})
