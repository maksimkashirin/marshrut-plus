from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SourceResponse(BaseModel):
    id: int
    region: str
    title: str
    url: str
    published_at: datetime | None
    checked_at: datetime

    model_config = ConfigDict(from_attributes=True)