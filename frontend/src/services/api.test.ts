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
})
