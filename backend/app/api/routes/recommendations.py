from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.recommendation import Recommendation


router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
)


@router.get("")
def get_recommendations(
    db: Session = Depends(get_db),
):
    recommendations = db.scalars(
        select(Recommendation).order_by(Recommendation.id)
    ).all()

    return [
        {
            "id": item.id,
            "code": item.code,
            "title": item.title,
            "description": item.description,
        }
        for item in recommendations
    ]