"""Database access for modeling jobs and their related artifacts."""

from uuid import UUID

from sqlmodel import Session, select

from app.models.modeling import (
    ModelingDraft,
    ModelingJob,
    ModelingJobStatus,
    ReviewedModelingResult,
    SourceBundle,
    WorkflowEvent,
    utc_now,
)
from app.schemas.modeling import (
    ModelingDraftCreate,
    ModelingJobCreate,
    ReviewedModelingResultCreate,
    SourceBundleCreate,
    WorkflowEventCreate,
)


class ModelingJobRepository:
    """Persists jobs, source bundles, drafts, review results, and workflow events."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create_job(self, data: ModelingJobCreate) -> ModelingJob:
        job = ModelingJob(game_name=data.game_name, steam_url=data.steam_url)
        self.session.add(job)
        self.session.commit()
        self.session.refresh(job)
        return job

    def get_job(self, job_id: UUID) -> ModelingJob | None:
        return self.session.get(ModelingJob, job_id)

    def get_source_bundle(self, job_id: UUID) -> SourceBundle | None:
        statement = select(SourceBundle).where(SourceBundle.job_id == job_id)
        return self.session.exec(statement).first()

    def get_modeling_draft(self, job_id: UUID) -> ModelingDraft | None:
        statement = select(ModelingDraft).where(ModelingDraft.job_id == job_id)
        return self.session.exec(statement).first()

    def get_reviewed_result(self, job_id: UUID) -> ReviewedModelingResult | None:
        statement = select(ReviewedModelingResult).where(ReviewedModelingResult.job_id == job_id)
        return self.session.exec(statement).first()

    def list_jobs(self) -> list[ModelingJob]:
        statement = select(ModelingJob).order_by(ModelingJob.created_at.desc())
        return list(self.session.exec(statement).all())

    def update_job_status(self, job: ModelingJob, status: ModelingJobStatus) -> ModelingJob:
        job.status = status
        job.updated_at = utc_now()
        self.session.add(job)
        self.session.commit()
        self.session.refresh(job)
        return job

    def save_source_bundle(self, job: ModelingJob, data: SourceBundleCreate) -> SourceBundle:
        source_bundle = self.get_source_bundle(job.id)
        if source_bundle is None:
            source_bundle = SourceBundle(job_id=job.id)
        source_bundle.raw_data = data.raw_data
        self.session.add(source_bundle)
        self.session.commit()
        self.session.refresh(source_bundle)
        return source_bundle

    def save_modeling_draft(self, job: ModelingJob, data: ModelingDraftCreate) -> ModelingDraft:
        draft = self.get_modeling_draft(job.id)
        if draft is None:
            draft = ModelingDraft(job_id=job.id)
        draft.raw_model_output = data.raw_model_output
        draft.validation_result = data.validation_result
        self.session.add(draft)
        self.session.commit()
        self.session.refresh(draft)
        return draft

    def save_reviewed_result(
        self,
        job: ModelingJob,
        data: ReviewedModelingResultCreate,
    ) -> ReviewedModelingResult:
        result = self.get_reviewed_result(job.id)
        if result is None:
            result = ReviewedModelingResult(job_id=job.id)
        result.reviewed_tags = data.reviewed_tags
        result.review_status = data.review_status
        result.reviewer_notes = data.reviewer_notes
        result.updated_at = utc_now()
        self.session.add(result)
        self.session.commit()
        self.session.refresh(result)
        return result

    def add_workflow_event(self, job: ModelingJob, data: WorkflowEventCreate) -> WorkflowEvent:
        event = WorkflowEvent(
            job_id=job.id,
            event_type=data.event_type,
            message=data.message,
            payload=data.payload,
        )
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event
