from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.modeling import ModelingJobStatus, ReviewStatus


class ModelingJobCreate(BaseModel):
    game_name: str = Field(min_length=1, max_length=255)
    steam_url: str = Field(min_length=1, max_length=2048)


class ModelingJobRead(BaseModel):
    id: UUID
    game_name: str
    steam_url: str
    status: ModelingJobStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SourceBundleCreate(BaseModel):
    raw_data: dict[str, Any] = Field(default_factory=dict)


class ModelingDraftCreate(BaseModel):
    raw_model_output: dict[str, Any] = Field(default_factory=dict)
    validation_result: dict[str, Any] = Field(default_factory=dict)


class ReviewedModelingResultCreate(BaseModel):
    reviewed_tags: dict[str, Any] = Field(default_factory=dict)
    review_status: ReviewStatus = ReviewStatus.DRAFT
    reviewer_notes: str | None = Field(default=None, max_length=5000)


class WorkflowEventCreate(BaseModel):
    event_type: str = Field(min_length=1, max_length=100)
    message: str | None = Field(default=None, max_length=2000)
    payload: dict[str, Any] = Field(default_factory=dict)
