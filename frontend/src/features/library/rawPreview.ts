export type RawPreviewMode = 'markdown' | 'text' | 'html' | 'pdf' | 'image' | 'unsupported'
export type RawMarkdownMetadata = Record<string, string>

export interface RawMarkdownDocument {
  frontmatter: RawMarkdownMetadata
  markdown: string
}

const MARKDOWN_EXTENSIONS = new Set(['md', 'markdown'])
const TEXT_EXTENSIONS = new Set([
  'txt',
  'text',
  'log',
  'csv',
  'tsv',
  'json',
  'jsonl',
  'json5',
  'xml',
  'yml',
  'yaml',
  'ini',
  'conf',
  'css',
  'js',
  'mjs',
  'cjs',
  'ts',
  'py',
  'sh',
  'bat',
  'ps1',
  'sql',
  'toml',
  'env',
  'cfg',
])
const HTML_EXTENSIONS = new Set(['html', 'htm'])
const IMAGE_EXTENSIONS = new Set(['png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'svg', 'ico', 'avif'])

export function getRawFileName(path: string): string {
  return path.split('/').pop() || path || 'raw-file'
}

function getExtension(path: string): string {
  const normalized = getRawFileName(path).toLowerCase()
  return normalized.includes('.') ? normalized.split('.').pop() ?? '' : ''
}

export function getRawPreviewMode(path: string): RawPreviewMode {
  const extension = getExtension(path)

  if (MARKDOWN_EXTENSIONS.has(extension)) return 'markdown'
  if (TEXT_EXTENSIONS.has(extension)) return 'text'
  if (HTML_EXTENSIONS.has(extension)) return 'html'
  if (extension === 'pdf') return 'pdf'
  if (IMAGE_EXTENSIONS.has(extension)) return 'image'
  return 'unsupported'
}

export function isTextRawPreview(mode: RawPreviewMode): boolean {
  return mode === 'markdown' || mode === 'text'
}

export function isInlineRawPreview(mode: RawPreviewMode): boolean {
  return mode !== 'unsupported'
}

function parseFrontmatterValue(value: string): string {
  const trimmed = value.trim()
  if (trimmed.length >= 2) {
    const quote = trimmed[0]
    if ((quote === '"' || quote === "'") && trimmed.at(-1) === quote) {
      return trimmed.slice(1, -1)
    }
  }
  return trimmed
}

export function parseRawMarkdown(source: string): RawMarkdownDocument {
  const normalized = source.replace(/^\uFEFF/, '')
  const match = normalized.match(/^---[ \t]*\r?\n([\s\S]*?)\r?\n---[ \t]*(?:\r?\n|$)/)
  if (!match) return { frontmatter: {}, markdown: source }

  const frontmatter: RawMarkdownMetadata = {}
  for (const line of match[1].split(/\r?\n/)) {
    const field = line.match(/^([A-Za-z0-9_-]+)\s*:\s*(.*)$/)
    if (field) frontmatter[field[1]] = parseFrontmatterValue(field[2])
  }

  return {
    frontmatter,
    markdown: normalized.slice(match[0].length).replace(/^\s*\r?\n/, ''),
  }
}
