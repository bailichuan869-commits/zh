import type { Component } from 'vue'
import {
  AppstoreOutlined,
  AuditOutlined,
  BankOutlined,
  BookOutlined,
  CompassOutlined,
  ExperimentOutlined,
  FileProtectOutlined,
  FolderOpenOutlined,
  ProfileOutlined,
  QuestionCircleOutlined,
  SafetyCertificateOutlined,
  ToolOutlined,
} from '@ant-design/icons-vue'
import type { NavigationDomain, NavigationTree } from '@/services/api'

export interface DomainMeta {
  icon: Component
  description: string
}

export const DOMAIN_ORDER = [
  'laws',
  'accounting-standards',
  'audit-standards',
  'policies',
  'ethics',
  'practice',
  'cases',
  'tools',
  'qa',
  'sources',
  'meta',
]

const domainMeta: Record<string, DomainMeta> = {
  laws: { icon: BankOutlined, description: '核心法律、条款目录与版本核验' },
  'accounting-standards': { icon: BookOutlined, description: '基本准则、具体准则、解释与应用资料' },
  'audit-standards': { icon: AuditOutlined, description: '执业准则、应用指南与审计方法' },
  policies: { icon: FileProtectOutlined, description: '财会监督、行业治理与事务所监管政策' },
  ethics: { icon: SafetyCertificateOutlined, description: '职业道德守则、独立性要求与行业史' },
  practice: { icon: ExperimentOutlined, description: '重点实务专题、审计流程与练习材料' },
  cases: { icon: ProfileOutlined, description: '按会计主题与审计风险整理的案例卡片' },
  tools: { icon: ToolOutlined, description: 'AI 编程、自动化工具与知识库助手' },
  qa: { icon: QuestionCircleOutlined, description: '已沉淀的专业问题与复核记录' },
  sources: { icon: FolderOpenOutlined, description: '来源批次、状态记录与原始资料索引' },
  meta: { icon: CompassOutlined, description: '知识库索引、总览与维护导航' },
}

const fallbackMeta: DomainMeta = {
  icon: AppstoreOutlined,
  description: '按主题整理的知识页面与原始资料',
}

export function getDomainMeta(key: string): DomainMeta {
  return domainMeta[key] ?? fallbackMeta
}

export function isBrowsablePath(path: string): boolean {
  return path.startsWith('wiki/') || path.startsWith('raw/')
}

export function sanitizeNavigationTree(tree: NavigationTree): NavigationTree {
  const domains = tree.domains.flatMap(domain => {
    const topics = domain.topics.flatMap(topic => {
      const pages = topic.pages.filter(page => isBrowsablePath(page.path))
      return pages.length ? [{ ...topic, count: pages.length, pages }] : []
    })
    const count = topics.reduce((sum, topic) => sum + topic.count, 0)
    return count ? [{ ...domain, count, topics }] : []
  })
  return { ...tree, domains }
}

export function orderDomains(domains: NavigationDomain[]): NavigationDomain[] {
  const positions = new Map(DOMAIN_ORDER.map((key, index) => [key, index]))
  return [...domains].sort((left, right) =>
    (positions.get(left.key) ?? DOMAIN_ORDER.length) - (positions.get(right.key) ?? DOMAIN_ORDER.length),
  )
}
