import type { CaseOverview } from './types'

const API_URL =
  import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

const CASE_ID =
  import.meta.env.VITE_DEMO_CASE_ID ?? '3'


export async function getCaseOverview(): Promise<CaseOverview> {
  const response = await fetch(
    `${API_URL}/cases/${CASE_ID}/overview`,
  )

  if (!response.ok) {
    throw new Error('Не удалось загрузить маршрут')
  }

  return response.json()
}


export async function completeStep(
  stepId: number,
): Promise<void> {
  const response = await fetch(
    `${API_URL}/steps/${stepId}`,
    {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        status: 'completed',
      }),
    },
  )

  if (!response.ok) {
    throw new Error('Не удалось сохранить шаг')
  }
}