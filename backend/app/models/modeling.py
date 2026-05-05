from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ModelingJobStatus(StrEnum):
    CREATED = "created"
    COLLECTING_SOURCES = "collecting_sources"
    MODELING = "modeling"
    VALIDATING = "validating"
    NEEDS_REVIEW = "needs_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPORTED = "exported"
    FAILED = "failed"


class ReviewStatus(StrEnum):
    DRAFT = "draft"
    NEEDS_REVIEW = "needs_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPORTED = "exported"


class ModelingJob(SQLModel, table=True):
    __tablename__ = "modeling_jobs"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    game_name: str = Field(index=True, min_length=1, max_length=255)
    steam_url: str = Field(min_length=1, max_length=2048)
    status: ModelingJobStatus = Field(
        default=ModelingJobStatus.CREATED,
        sa_column=Column(
            Enum(
                ModelingJobStatus,
                values_callable=lambda enum: [item.value for item in enum],
                name="modeling_job_status",
            ),
            nullable=False,
            index=True,
        ),
    )
    created_at: datetime = Field(default_factory=utc_now, sa_column=Column(DateTime(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=utc_now, sa_column=Column(DateTime(timezone=True), nullable=False))

    source_bundles: list["SourceBundle"] = Relationship(back_populates="job")
    modeling_drafts: list["ModelingDraft"] = Relationship(back_populates="job")
    reviewed_results: list["ReviewedModelingResult"] = Relationship(back_populates="job")
    workflow_events: list["WorkflowEvent"] = Relationship(back_populates="job")


class SourceBundle(SQLModel, table=True):
    __tablename__ = "source_bundles"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    job_id: UUID = Field(foreign_key="modeling_jobs.id", index=True, unique=True)
    raw_data: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB, nullable=False))
    created_at: datetime = Field(default_factory=utc_now, sa_column=Column(DateTime(timezone=True), nullable=False))

    job: ModelingJob = Relationship(back_populates="source_bundles")


class ModelingDraft(SQLModel, table=True):
    __tablename__ = "modeling_drafts"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    job_id: UUID = Field(foreign_key="modeling_jobs.id", index=True, unique=True)
    raw_model_output: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB, nullable=False))
    validation_result: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB, nullable=False))
    created_at: datetime = Field(default_factory=utc_now, sa_column=Column(DateTime(timezone=True), nullable=False))

    job: ModelingJob = Relationship(back_populates="modeling_drafts")


class ReviewedModelingResult(SQLModel, table=True):
    __tablename__ = "reviewed_modeling_results"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    job_id: UUID = Field(foreign_key="modeling_jobs.id", index=True, unique=True)
    reviewed_tags: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB, nullable=False))
    review_status: ReviewStatus = Field(
        default=ReviewStatus.DRAFT,
        sa_column=Column(
            Enum(
                ReviewStatus,
                values_callable=lambda enum: [item.value for item in enum],
                name="review_status",
            ),
            nullable=False,
            index=True,
        ),
    )
    reviewer_notes: str | None = Field(default=None, max_length=5000)
    created_at: datetime = Field(default_factory=utc_now, sa_column=Column(DateTime(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=utc_now, sa_column=Column(DateTime(timezone=True), nullable=False))

    job: ModelingJob = Relationship(back_populates="reviewed_results")


class WorkflowEvent(SQLModel, table=True):
    __tablename__ = "workflow_events"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    job_id: UUID = Field(foreign_key="modeling_jobs.id", index=True)
    event_type: str = Field(index=True, min_length=1, max_length=100)
    message: str | None = Field(default=None, max_length=2000)
    payload: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB, nullable=False))
    created_at: datetime = Field(default_factory=utc_now, sa_column=Column(DateTime(timezone=True), nullable=False))

    job: ModelingJob = Relationship(back_populates="workflow_events")
