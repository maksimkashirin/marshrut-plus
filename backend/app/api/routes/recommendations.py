from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.recommendation import Recommendation
from app.schemas.recommendation import RecommendationResponse


router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
)


@router.get(
    "",
    response_model=list[RecommendationResponse],
)
def get_recommendations(
    db: Session = Depends(get_db),
):
    return db.scalars(
        select(Recommendation).order_by(Recommendation.id)
    ).all()
