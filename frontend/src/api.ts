import type {
  CaseOverview,
  Recommendation,
} from './types'


const API_URL =
  import.meta.env.VITE_API_URL ?? 'http://localhost:8000'


export async function getRecommendations(): Promise<Recommendation[]> {
  const response = await fetch(
    `${API_URL}/recommendations`,
  )

  if (!response.ok) {
    throw new Error(
      'Не удалось загрузить рекомендации',
    )
  }

  return response.json()
}


export async function createUser(
  maxUserId: string,
): Promise<{ id: number }> {
  const response = await fetch(
    `${API_URL}/users`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        max_user_id: maxUserId,
      }),
    },
  )

  if (!response.ok) {
    throw new Error(
      'Не удалось создать пользователя',
    )
  }

  return response.json()
}


export async function createCase(
  userId: number,
  recommendationCodes: string[],
): Promise<{ id: number }> {
  const response = await fetch(
    `${API_URL}/cases`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        region: 'Хабаровский край',
        recommendation_codes:
          recommendationCodes,
      }),
    },
  )

  if (!response.ok) {
    throw new Error(
      'Не удалось создать маршрут',
    )
  }

  return response.json()
}


export async function getCaseOverview(
  caseId: number,
): Promise<CaseOverview> {
  const response = await fetch(
    `${API_URL}/cases/${caseId}/overview`,
  )

  if (!response.ok) {
    throw new Error(
      'Не удалось загрузить маршрут',
    )
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
    throw new Error(
      'Не удалось сохранить шаг',
    )
  }
}