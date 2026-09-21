from pydantic import BaseModel, ConfigDict


class RecommendationResponse(BaseModel):
    id: int
    code: str
    title: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)