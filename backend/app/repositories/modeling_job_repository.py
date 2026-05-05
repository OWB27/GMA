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
        source_bundle = SourceBundle(job_id=job.id, raw_data=data.raw_data)
        self.session.add(source_bundle)
        self.session.commit()
        self.session.refresh(source_bundle)
        return source_bundle

    def save_modeling_draft(self, job: ModelingJob, data: ModelingDraftCreate) -> ModelingDraft:
        draft = ModelingDraft(
            job_id=job.id,
            raw_model_output=data.raw_model_output,
            validation_result=data.validation_result,
        )
        self.session.add(draft)
        self.session.commit()
        self.session.refresh(draft)
        return draft

    def save_reviewed_result(
        self,
        job: ModelingJob,
        data: ReviewedModelingResultCreate,
    ) -> ReviewedModelingResult:
        result = ReviewedModelingResult(
            job_id=job.id,
            reviewed_tags=data.reviewed_tags,
            review_status=data.review_status,
            reviewer_notes=data.reviewer_notes,
        )
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
