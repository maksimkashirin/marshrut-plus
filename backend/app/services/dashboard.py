from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case import Case
from app.models.route_step import RouteStep
from app.models.source import Source
from app.schemas.route_step import (
    RouteDashboardResponse,
    RouteStepDetail,
)


def build_case_dashboard(
    db: Session,
    case: Case,
) -> RouteDashboardResponse:
    steps = list(
        db.scalars(
            select(RouteStep)
            .where(RouteStep.case_id == case.id)
            .order_by(RouteStep.order_number)
        ).all()
    )

    total_steps = len(steps)

    completed_steps = sum(
        1
        for step in steps
        if step.status == "completed"
    )

    if total_steps == 0:
        progress_percent = 0
    else:
        progress_percent = round(
            completed_steps / total_steps * 100
        )

    source_ids = {
        step.source_id
        for step in steps
        if step.source_id is not None
    }

    sources = {}

    if source_ids:
        source_list = db.scalars(
            select(Source).where(
                Source.id.in_(source_ids)
            )
        ).all()

        sources = {
            source.id: source
            for source in source_list
        }

    detailed_steps = []

    for step in steps:
        source = (
            sources.get(step.source_id)
            if step.source_id is not None
            else None
        )

        detailed_steps.append(
            RouteStepDetail(
                id=step.id,
                case_id=step.case_id,
                source_id=step.source_id,
                step_code=step.step_code,
                title=step.title,
                description=step.description,
                order_number=step.order_number,
                status=step.status,
                completed_at=step.completed_at,
                source=source,
            )
        )

    next_step = next(
        (
            step
            for step in detailed_steps
            if step.status != "completed"
        ),
        None,
    )

    return RouteDashboardResponse(
        case_id=case.id,
        case_status=case.status,
        total_steps=total_steps,
        completed_steps=completed_steps,
        progress_percent=progress_percent,
        next_step=next_step,
        steps=detailed_steps,
    )