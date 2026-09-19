from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    max_user_id: str | None = None


class UserResponse(BaseModel):
    id: int
    max_user_id: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)