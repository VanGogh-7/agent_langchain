from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ResourceStatus(StrEnum):
    planned = "planned"
    reading = "reading"
    finished = "finished"
    archived = "archived"


class ResourceBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str | None = Field(default=None, max_length=200)
    category: str | None = Field(default=None, max_length=100)
    status: ResourceStatus = ResourceStatus.planned
    rating: int | None = Field(default=None, ge=1, le=5)
    notes: str | None = None

    @field_validator("title")
    @classmethod
    def title_cannot_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Title cannot be empty")
        return value.strip()


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, max_length=200)
    category: str | None = Field(default=None, max_length=100)
    status: ResourceStatus | None = None
    rating: int | None = Field(default=None, ge=1, le=5)
    notes: str | None = None

    @field_validator("title")
    @classmethod
    def title_cannot_be_blank(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("Title cannot be empty")
        return value.strip() if value is not None else value


class ResourceRead(ResourceBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
