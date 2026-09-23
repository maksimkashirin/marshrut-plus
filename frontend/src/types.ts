export interface Source {
  id: number
  region: string
  title: string
  url: string
  published_at: string | null
  checked_at: string
}

export interface RouteStep {
  id: number
  case_id: number
  source_id: number | null
  step_code: string
  title: string
  description: string | null
  order_number: number
  status: string
  completed_at: string | null
  source: Source | null
}

export interface Recommendation {
  id: number
  code: string
  title: string
  description: string | null
}

export interface CaseInfo {
  id: number
  user_id: number
  region: string
  status: string
  created_at: string
}

export interface Dashboard {
  case_id: number
  case_status: string
  total_steps: number
  completed_steps: number
  progress_percent: number
  next_step: RouteStep | null
  steps: RouteStep[]
}

export interface CaseOverview {
  case: CaseInfo
  recommendations: Recommendation[]
  dashboard: Dashboard
}