from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# Input Schema (Client -> API)
class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    description: Optional[str] = None


# Output Schema (API -> Client)
class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    owner_id: int
    updated_at: datetime
    created_at: datetime


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = None
    completed: bool | None = None
