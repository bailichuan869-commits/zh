const removableExtensions = /(?:\.(?:md|pdf|docx?|xlsx?|pptx?|html?|txt|csv))+$/gi
const numericPrefix = /^\d{2,4}[-_\s]+/
const sectionHeading = /^(?:第[一二三四五六七八九十百\d]+[章节部分]|[一二三四五六七八九十]+、)/

export function cleanDisplayTitle(value: string, path = ''): string {
  const fallback = path.split('/').pop() ?? ''
  return (value.trim() || fallback)
    .replace(removableExtensions, '')
    .replace(numericPrefix, '')
    .replace(/[_]+/g, ' ')
    .replace(/\s+/g, ' ')
    .replace(/[.。·\-_\s]+$/g, '')
    .trim()
}

export function isWeakTitle(value: string): boolean {
  const semantic = value.replace(/[\d\s.。·\-_()（）]+/g, '')
  return semantic.length < 4
}

export function extractReadableTitle(markdown: string): string {
  const headings = markdown
    .split(/\r?\n/)
    .map(line => line.match(/^#{1,3}\s+(.+)$/)?.[1]?.trim() ?? '')
    .filter(Boolean)

  const parts: string[] = []
  for (const heading of headings) {
    const cleaned = cleanDisplayTitle(heading)
    if (isWeakTitle(cleaned)) continue
    if (parts.length && sectionHeading.test(cleaned)) break
    parts.push(cleaned)
    if (parts.length >= 3) break
  }

  return parts
    .join('')
    .replace(/\s+(?=[号》])/g, '')
    .replace(/号——(?=对|财|审|其|关)/g, '号——')
    .trim()
}
