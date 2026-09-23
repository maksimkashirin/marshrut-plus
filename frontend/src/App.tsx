import { useEffect, useState } from 'react'

import './App.css'

import {
  completeStep,
  getCaseOverview,
} from './api'

import type {
  CaseOverview,
} from './types'


function App() {
  const [data, setData] =
    useState<CaseOverview | null>(null)

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState<string | null>(null)

  const [saving, setSaving] =
    useState(false)


  async function loadOverview() {
    try {
      setError(null)

      const overview =
        await getCaseOverview()

      setData(overview)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Произошла ошибка',
      )
    } finally {
      setLoading(false)
    }
  }


  useEffect(() => {
    loadOverview()
  }, [])


  async function handleCompleteStep() {
    const step = data?.dashboard.next_step

    if (!step) {
      return
    }

    try {
      setSaving(true)

      await completeStep(step.id)

      await loadOverview()
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


  if (loading) {
    return (
      <main className="page">
        <p>Загружаем маршрут...</p>
      </main>
    )
  }


  if (error || !data) {
    return (
      <main className="page">
        <div className="card">
          <h1>Маршрут+</h1>

          <p className="error">
            {error ?? 'Нет данных'}
          </p>

          <button onClick={loadOverview}>
            Повторить
          </button>
        </div>
      </main>
    )
  }


  const dashboard = data.dashboard


  return (
    <main className="page">
      <header className="header">
        <div>
          <span className="eyebrow">
            После ПМПК
          </span>

          <h1>Маршрут+</h1>

          <p>{data.case.region}</p>
        </div>

        <div className="status">
          Активный маршрут
        </div>
      </header>


      <section className="card progress-card">
        <div className="section-heading">
          <div>
            <span className="label">
              Ваш прогресс
            </span>

            <strong>
              {dashboard.completed_steps}
              {' из '}
              {dashboard.total_steps}
              {' шагов'}
            </strong>
          </div>

          <span className="percent">
            {dashboard.progress_percent}%
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
            {dashboard.next_step.title}
          </h2>

          <p>
            {dashboard.next_step.description}
          </p>

          {dashboard.next_step.source && (
            <a
              href={
                dashboard.next_step.source.url
              }
              target="_blank"
              rel="noreferrer"
            >
              Официальный источник ↗
            </a>
          )}

          <button
            onClick={handleCompleteStep}
            disabled={saving}
          >
            {saving
              ? 'Сохраняем...'
              : 'Отметить выполненным'}
          </button>
        </section>
      ) : (
        <section className="card">
          <h2>Маршрут завершён 🎉</h2>

          <p>
            Все запланированные действия
            отмечены как выполненные.
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
                  {recommendation.title}
                </strong>

                {recommendation.description && (
                  <p>
                    {recommendation.description}
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
          {dashboard.steps.map((step) => {
            const completed =
              step.status === 'completed'

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
          })}
        </div>
      </section>
    </main>
  )
}

export default App