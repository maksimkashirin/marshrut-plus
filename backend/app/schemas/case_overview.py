from pydantic import BaseModel

from app.schemas.case import CaseResponse
from app.schemas.recommendation import RecommendationResponse
from app.schemas.route_step import RouteDashboardResponse


class CaseOverviewResponse(BaseModel):
    case: CaseResponse
    recommendations: list[RecommendationResponse]
    dashboard: RouteDashboardResponse