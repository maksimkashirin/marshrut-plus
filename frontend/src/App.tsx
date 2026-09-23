import {
  useEffect,
  useState,
} from 'react'

import './App.css'

import {
  completeStep,
  createCase,
  createUser,
  getCaseOverview,
  getRecommendations,
} from './api'

import type {
  CaseOverview,
  Recommendation,
} from './types'


const CASE_STORAGE_KEY =
  'marshrut_plus_case_id'

const USER_STORAGE_KEY =
  'marshrut_plus_demo_user'


function getDemoUserId(): string {
  let id = localStorage.getItem(
    USER_STORAGE_KEY,
  )

  if (!id) {
    id = `web_demo_${crypto.randomUUID()}`

    localStorage.setItem(
      USER_STORAGE_KEY,
      id,
    )
  }

  return id
}


function App() {
  const [data, setData] =
    useState<CaseOverview | null>(null)

  const [recommendations, setRecommendations] =
    useState<Recommendation[]>([])

  const [selectedCodes, setSelectedCodes] =
    useState<string[]>([])

  const [loading, setLoading] =
    useState(true)

  const [creating, setCreating] =
    useState(false)

  const [saving, setSaving] =
    useState(false)

  const [error, setError] =
    useState<string | null>(null)


  async function loadExistingCase() {
    const storedCaseId =
      localStorage.getItem(
        CASE_STORAGE_KEY,
      )

    if (!storedCaseId) {
      setLoading(false)
      return
    }

    try {
      const overview =
        await getCaseOverview(
          Number(storedCaseId),
        )

      setData(overview)
    } catch {
      localStorage.removeItem(
        CASE_STORAGE_KEY,
      )
    } finally {
      setLoading(false)
    }
  }


  async function loadRecommendations() {
    try {
      const items =
        await getRecommendations()

      setRecommendations(items)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Ошибка загрузки',
      )
    }
  }


  useEffect(() => {
    loadExistingCase()
    loadRecommendations()
  }, [])


  function toggleRecommendation(
    code: string,
  ) {
    setSelectedCodes(
      (current) =>
        current.includes(code)
          ? current.filter(
              (item) => item !== code,
            )
          : [...current, code],
    )
  }


  async function handleCreateRoute() {
    if (selectedCodes.length === 0) {
      setError(
        'Выберите хотя бы одну рекомендацию',
      )
      return
    }

    try {
      setCreating(true)
      setError(null)

      const demoUserId =
        getDemoUserId()

      const user =
        await createUser(
          demoUserId,
        )

      const newCase =
        await createCase(
          user.id,
          selectedCodes,
        )

      localStorage.setItem(
        CASE_STORAGE_KEY,
        String(newCase.id),
      )

      const overview =
        await getCaseOverview(
          newCase.id,
        )

      setData(overview)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Не удалось создать маршрут',
      )
    } finally {
      setCreating(false)
    }
  }


  async function loadOverview(
    caseId: number,
  ) {
    try {
      const overview =
        await getCaseOverview(
          caseId,
        )

      setData(overview)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Ошибка загрузки',
      )
    }
  }


  async function handleCompleteStep() {
    const step =
      data?.dashboard.next_step

    if (!step || !data) {
      return
    }

    try {
      setSaving(true)

      await completeStep(
        step.id,
      )

      await loadOverview(
        data.case.id,
      )
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Не удалось сохранить шаг',
      )
    } finally {
      setSaving(false)
    }
  }


  function resetDemo() {
    localStorage.removeItem(
      CASE_STORAGE_KEY,
    )

    setData(null)
    setSelectedCodes([])
    setError(null)
  }


  if (loading) {
    return (
      <main className="page">
        <p>Загружаем Маршрут+...</p>
      </main>
    )
  }


  if (!data) {
    return (
      <main className="page onboarding">
        <header className="welcome">
          <span className="eyebrow">
            После ПМПК
          </span>

          <h1>Маршрут+</h1>

          <p>
            Поможем пройти путь после
            получения заключения ПМПК:
            от первого действия до
            понятного плана сопровождения.
          </p>
        </header>


        <section className="card">
          <span className="label">
            Шаг 1
          </span>

          <h2>
            Заключение ПМПК уже получено?
          </h2>

          <p>
            Этот сервис предназначен для
            родителей, которые уже получили
            заключение и решили использовать
            рекомендации.
          </p>

          <div className="confirmation">
            ✓ Да, заключение уже получено
          </div>
        </section>


        <section>
          <h2 className="section-title">
            Что рекомендовано?
          </h2>

          <p className="section-description">
            Для демонстрации выберите
            рекомендации из тестового
            заключения.
          </p>

          <div className="recommendation-picker">
            {recommendations.map(
              (recommendation) => {
                const selected =
                  selectedCodes.includes(
                    recommendation.code,
                  )

                return (
                  <button
                    type="button"
                    key={
                      recommendation.id
                    }
                    className={
                      selected
                        ? 'picker-card selected'
                        : 'picker-card'
                    }
                    onClick={() =>
                      toggleRecommendation(
                        recommendation.code,
                      )
                    }
                  >
                    <span className="picker-check">
                      {selected
                        ? '✓'
                        : ''}
                    </span>

                    <span>
                      <strong>
                        {
                          recommendation.title
                        }
                      </strong>

                      <small>
                        {
                          recommendation.description
                        }
                      </small>
                    </span>
                  </button>
                )
              },
            )}
          </div>
        </section>


        {error && (
          <p className="error">
            {error}
          </p>
        )}


        <button
          className="create-route-button"
          onClick={handleCreateRoute}
          disabled={creating}
        >
          {creating
            ? 'Создаём маршрут...'
            : 'Создать мой маршрут'}
        </button>
      </main>
    )
  }


  const dashboard =
    data.dashboard


  return (
    <main className="page">
      <header className="header">
        <div>
          <span className="eyebrow">
            После ПМПК
          </span>

          <h1>Маршрут+</h1>

          <p>
            {data.case.region}
          </p>
        </div>

        <div className="status">
          {dashboard.case_status ===
          'completed'
            ? 'Маршрут завершён'
            : 'Активный маршрут'}
        </div>
      </header>


      <section className="card progress-card">
        <div className="section-heading">
          <div>
            <span className="label">
              Ваш прогресс
            </span>

            <strong>
              {
                dashboard.completed_steps
              }
              {' из '}
              {dashboard.total_steps}
              {' шагов'}
            </strong>
          </div>

          <span className="percent">
            {
              dashboard.progress_percent
            }
            %
          </span>
        </div>

        <div className="progress-track">
          <div
            className="progress-value"
            style={{
              width:
                `${dashboard.progress_percent}%`,
            }}
          />
        </div>
      </section>


      {dashboard.next_step ? (
        <section className="card next-card">
          <span className="label">
            Следующий шаг
          </span>

          <h2>
            {
              dashboard.next_step.title
            }
          </h2>

          <p>
            {
              dashboard.next_step
                .description
            }
          </p>

          {dashboard.next_step.source && (
            <a
              href={
                dashboard.next_step
                  .source.url
              }
              target="_blank"
              rel="noreferrer"
            >
              Официальный источник ↗
            </a>
          )}

          <button
            onClick={
              handleCompleteStep
            }
            disabled={saving}
          >
            {saving
              ? 'Сохраняем...'
              : 'Отметить выполненным'}
          </button>
        </section>
      ) : (
        <section className="card">
          <h2>
            Маршрут завершён 🎉
          </h2>

          <p>
            Все действия отмечены
            как выполненные.
          </p>
        </section>
      )}


      <section>
        <h2 className="section-title">
          Ваши рекомендации
        </h2>

        <div className="recommendations">
          {data.recommendations.map(
            (recommendation) => (
              <article
                className="recommendation"
                key={recommendation.id}
              >
                <strong>
                  {
                    recommendation.title
                  }
                </strong>

                {recommendation.description && (
                  <p>
                    {
                      recommendation.description
                    }
                  </p>
                )}
              </article>
            ),
          )}
        </div>
      </section>


      <section>
        <h2 className="section-title">
          Мой маршрут
        </h2>

        <div className="steps">
          {dashboard.steps.map(
            (step) => {
              const completed =
                step.status ===
                'completed'

              return (
                <article
                  className={
                    completed
                      ? 'step completed'
                      : 'step'
                  }
                  key={step.id}
                >
                  <div className="step-number">
                    {completed
                      ? '✓'
                      : step.order_number}
                  </div>

                  <div>
                    <strong>
                      {step.title}
                    </strong>

                    <p>
                      {completed
                        ? 'Выполнено'
                        : 'Предстоит выполнить'}
                    </p>
                  </div>
                </article>
              )
            },
          )}
        </div>
      </section>


      <button
        className="reset-button"
        onClick={resetDemo}
      >
        Начать демо заново
      </button>
    </main>
  )
}

export default App