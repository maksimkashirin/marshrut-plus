from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CaseCreate(BaseModel):
    user_id: int
    region: str
    recommendation_codes: list[str] = Field(default_factory=list)


class CaseResponse(BaseModel):
    id: int
    user_id: int
    region: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)