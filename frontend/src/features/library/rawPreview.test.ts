import { describe, expect, it } from 'vitest'
import {
  getRawFileName,
  getRawPreviewMode,
  isInlineRawPreview,
  isTextRawPreview,
  parseRawMarkdown,
} from './rawPreview'

describe('raw preview helpers', () => {
  it('classifies markdown and plain text files for inline reading', () => {
    expect(getRawPreviewMode('raw/laws/example.md')).toBe('markdown')
    expect(getRawPreviewMode('raw/laws/example.txt')).toBe('text')
    expect(getRawPreviewMode('raw/laws/example.json')).toBe('text')
  })

  it('classifies browser-embeddable assets separately from downloads', () => {
    expect(getRawPreviewMode('raw/laws/example.html')).toBe('html')
    expect(getRawPreviewMode('raw/laws/example.pdf')).toBe('pdf')
    expect(getRawPreviewMode('raw/laws/example.png')).toBe('image')
    expect(getRawPreviewMode('raw/laws/example.zip')).toBe('unsupported')
  })

  it('exposes simple mode predicates and file names', () => {
    expect(isTextRawPreview('markdown')).toBe(true)
    expect(isTextRawPreview('pdf')).toBe(false)
    expect(isInlineRawPreview('image')).toBe(true)
    expect(isInlineRawPreview('unsupported')).toBe(false)
    expect(getRawFileName('raw/laws/example.pdf')).toBe('example.pdf')
  })

  it('separates YAML frontmatter from rendered markdown', () => {
    const parsed = parseRawMarkdown(`---
title: "所得税准则应用案例"
source_type: 'web-snapshot'
source_role: index-page
index_item_count: 1
---

# 所得税准则应用案例

正文内容
`)

    expect(parsed.frontmatter).toEqual({
      title: '所得税准则应用案例',
      source_type: 'web-snapshot',
      source_role: 'index-page',
      index_item_count: '1',
    })
    expect(parsed.markdown).toBe('# 所得税准则应用案例\n\n正文内容\n')
    expect(parsed.markdown).not.toContain('source_role')
  })

  it('leaves markdown without frontmatter unchanged', () => {
    const source = '# 普通正文\n\n内容'
    expect(parseRawMarkdown(source)).toEqual({ frontmatter: {}, markdown: source })
  })
})
