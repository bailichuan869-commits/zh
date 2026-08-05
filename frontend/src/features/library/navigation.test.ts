import { describe, expect, it } from 'vitest'
import { isBrowsablePath, orderDomains, sanitizeNavigationTree } from './navigation'
import { cleanDisplayTitle, extractReadableTitle, isWeakTitle } from './titles'
import type { NavigationTree } from '@/services/api'

describe('knowledge navigation helpers', () => {
  it('keeps only paths that the read-only frontend can open', () => {
    expect(isBrowsablePath('wiki/concepts/example.md')).toBe(true)
    expect(isBrowsablePath('raw/standards/example.pdf.md')).toBe(true)
    expect(isBrowsablePath('raw/standards/example.html.structure.json')).toBe(false)
    expect(isBrowsablePath('raw/standards/example.html.structure-4fdd85ec.json')).toBe(false)
    expect(isBrowsablePath('cache/pdf-markdown/files/example.md')).toBe(false)
  })

  it('removes internal cache pages and recomputes visible counts', () => {
    const tree: NavigationTree = {
      generated: '2026-08-04T13:10:42',
      domains: [{
        key: 'audit-standards',
        label: '审计准则',
        icon: '',
        count: 2,
        topics: [{
          key: 'raw-audit',
          label: '原文资料',
          count: 2,
          pages: [
            { path: 'raw/a.md', title: 'A', short: '', kind: 'raw', type: 'md', updated: '', page_role: '', maturity: '', answer_ready: false },
            { path: 'cache/a.md', title: 'A', short: '', kind: 'cache', type: 'md', updated: '', page_role: '', maturity: '', answer_ready: false },
          ],
        }],
      }],
    }

    const sanitized = sanitizeNavigationTree(tree)
    expect(sanitized.domains[0].count).toBe(1)
    expect(sanitized.domains[0].topics[0].count).toBe(1)
    expect(sanitized.domains[0].topics[0].pages[0].path).toBe('raw/a.md')
  })

  it('uses the professional reading order', () => {
    const domains = [
      { key: 'audit-standards', label: '审计准则', icon: '', count: 0, topics: [] },
      { key: 'laws', label: '法律法规', icon: '', count: 0, topics: [] },
    ]
    expect(orderDomains(domains).map(item => item.key)).toEqual(['laws', 'audit-standards'])
  })
})

describe('search result titles', () => {
  it('removes download numbers and chained file extensions', () => {
    expect(cleanDisplayTitle('058-中国注册会计师审阅准则第2101号-财务报表审阅-应用指南.pdf', ''))
      .toBe('中国注册会计师审阅准则第2101号-财务报表审阅-应用指南')
  })

  it('detects numeric placeholder titles', () => {
    expect(isWeakTitle(cleanDisplayTitle('21..pdf'))).toBe(true)
  })

  it('combines split source headings into a readable title', () => {
    const markdown = '# 21.\n\n## 《中国注册会计师审计准则第1401 号——\n\n## 对集团财务报表审计的特殊考虑》\n\n## 应用指南\n\n## 一、定义'
    expect(extractReadableTitle(markdown)).toBe('《中国注册会计师审计准则第1401号——对集团财务报表审计的特殊考虑》应用指南')
  })
})
