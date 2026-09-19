from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.schemas.source import SourceResponse


class RouteStepResponse(BaseModel):
    id: int
    case_id: int
    source_id: int | None
    step_code: str
    title: str
    description: str | None
    order_number: int
    status: str
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class RouteStepUpdate(BaseModel):
    status: Literal["pending", "completed"]


class RouteStepDetail(RouteStepResponse):
    source: SourceResponse | None = None


class RouteDashboardResponse(BaseModel):
    case_id: int
    case_status: str

    total_steps: int
    completed_steps: int
    progress_percent: int

    next_step: RouteStepDetail | None

    steps: list[RouteStepDetail]