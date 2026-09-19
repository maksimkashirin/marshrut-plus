from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.case import Case
from app.models.route_step import RouteStep
from app.models.source import Source
from app.schemas.route_step import (
    RouteDashboardResponse,
    RouteStepDetail,
    RouteStepResponse,
    RouteStepUpdate,
)


router = APIRouter(
    tags=["route"],
)


@router.get(
    "/cases/{case_id}/route",
    response_model=list[RouteStepResponse],
)
def get_case_route(
    case_id: int,
    db: Session = Depends(get_db),
):
    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    steps = db.scalars(
        select(RouteStep)
        .where(RouteStep.case_id == case_id)
        .order_by(RouteStep.order_number)
    ).all()

    return list(steps)


@router.get(
    "/cases/{case_id}/dashboard",
    response_model=RouteDashboardResponse,
)
def get_case_dashboard(
    case_id: int,
    db: Session = Depends(get_db),
):
    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    steps = list(
        db.scalars(
            select(RouteStep)
            .where(RouteStep.case_id == case_id)
            .order_by(RouteStep.order_number)
        ).all()
    )

    total_steps = len(steps)

    completed_steps = sum(
        1 for step in steps
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
            select(Source).where(Source.id.in_(source_ids))
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


@router.patch(
    "/steps/{step_id}",
    response_model=RouteStepResponse,
)
def update_step(
    step_id: int,
    data: RouteStepUpdate,
    db: Session = Depends(get_db),
):
    step = db.get(RouteStep, step_id)

    if step is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route step not found",
        )

    step.status = data.status

    if data.status == "completed":
        step.completed_at = datetime.now(timezone.utc)
    else:
        step.completed_at = None

    # Сохраняем изменение в текущей транзакции,
    # чтобы следующий запрос к БД уже видел новый статус.
    db.flush()

    remaining_steps = db.scalar(
        select(func.count())
        .select_from(RouteStep)
        .where(
            RouteStep.case_id == step.case_id,
            RouteStep.status != "completed",
        )
    )

    case = db.get(Case, step.case_id)

    if case is not None:
        if remaining_steps == 0:
            case.status = "completed"
        else:
            case.status = "active"

    db.commit()
    db.refresh(step)

    return step