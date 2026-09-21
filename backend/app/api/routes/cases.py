from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.recommendation import RecommendationResponse
from app.schemas.case_overview import CaseOverviewResponse
from app.services.dashboard import build_case_dashboard

from app.database import get_db
from app.models.case import Case
from app.models.case_recommendation import CaseRecommendation
from app.models.recommendation import Recommendation
from app.models.user import User
from app.schemas.case import CaseCreate, CaseResponse
from app.services.route_engine import create_route_for_case


router = APIRouter(
    prefix="/cases",
    tags=["cases"],
)


@router.post(
    "",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_case(
    data: CaseCreate,
    db: Session = Depends(get_db),
):
    user = db.get(User, data.user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    recommendation_codes = list(
        dict.fromkeys(data.recommendation_codes)
    )

    recommendations = []

    if recommendation_codes:
        recommendations = list(
            db.scalars(
                select(Recommendation).where(
                    Recommendation.code.in_(
                        recommendation_codes
                    )
                )
            ).all()
        )

        found_codes = {
            recommendation.code
            for recommendation in recommendations
        }

        missing_codes = [
            code
            for code in recommendation_codes
            if code not in found_codes
        ]

        if missing_codes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Unknown recommendation codes: "
                    + ", ".join(missing_codes)
                ),
            )

    case = Case(
        user_id=data.user_id,
        region=data.region,
        status="active",
    )

    db.add(case)
    db.flush()

    for recommendation in recommendations:
        link = CaseRecommendation(
            case_id=case.id,
            recommendation_id=recommendation.id,
        )

        db.add(link)

    try:
        create_route_for_case(
            db=db,
            case_id=case.id,
            region=case.region,
            recommendation_codes=recommendation_codes,
        )

    except ValueError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    db.commit()
    db.refresh(case)

    return case


@router.get(
    "/{case_id}",
    response_model=CaseResponse,
)
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
):
    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    return case


@router.get(
    "/{case_id}",
    response_model=CaseResponse,
)
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
):
    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    return case

@router.get(
    "/{case_id}/recommendations",
    response_model=list[RecommendationResponse],
)
def get_case_recommendations(
    case_id: int,
    db: Session = Depends(get_db),
):
    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    recommendations = db.scalars(
        select(Recommendation)
        .join(
            CaseRecommendation,
            CaseRecommendation.recommendation_id
            == Recommendation.id,
        )
        .where(
            CaseRecommendation.case_id == case_id
        )
        .order_by(Recommendation.id)
    ).all()

    return list(recommendations)

@router.get(
    "/{case_id}/overview",
    response_model=CaseOverviewResponse,
)
def get_case_overview(
    case_id: int,
    db: Session = Depends(get_db),
):
    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    recommendations = list(
        db.scalars(
            select(Recommendation)
            .join(
                CaseRecommendation,
                CaseRecommendation.recommendation_id
                == Recommendation.id,
            )
            .where(
                CaseRecommendation.case_id == case_id
            )
            .order_by(Recommendation.id)
        ).all()
    )

    dashboard = build_case_dashboard(
        db=db,
        case=case,
    )

    return CaseOverviewResponse(
        case=case,
        recommendations=recommendations,
        dashboard=dashboard,
    )