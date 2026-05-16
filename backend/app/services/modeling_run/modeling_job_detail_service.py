"""Read-only use case for rebuilding a persisted modeling run response."""

from uuid import UUID

from app.repositories.modeling_job_repository import ModelingJobRepository
from app.schemas.modeling_run import ModelingRunResponse


class ModelingJobNotFoundError(Exception):
    """Raised when a requested modeling job does not exist."""


class ModelingJobDetailService:
    """Loads a saved modeling job and its artifacts for frontend display."""

    def __init__(self, repository: ModelingJobRepository) -> None:
        self.repository = repository

    def get_job_detail(self, job_id: UUID) -> ModelingRunResponse:
        job = self.repository.get_job(job_id)
        if job is None:
            raise ModelingJobNotFoundError("Modeling job not found.")

        source_bundle = self.repository.get_source_bundle(job_id)
        modeling_draft = self.repository.get_modeling_draft(job_id)
        workflow_finished = self.repository.get_latest_workflow_event(job_id, "workflow_finished")
        workflow_payload = workflow_finished.payload if workflow_finished is not None else {}

        return ModelingRunResponse(
            job_id=str(job.id),
            game_name=job.game_name,
            steam_url=job.steam_url,
            source_bundle=source_bundle.raw_data if source_bundle is not None else None,
            source_assessment=workflow_payload.get("source_assessment"),
            retrieved_context=None,
            modeling_result=modeling_draft.raw_model_output if modeling_draft is not None else None,
            validation_result=modeling_draft.validation_result if modeling_draft is not None else None,
            status=job.status.value,
            errors=workflow_payload.get("errors", []),
            trace=workflow_payload.get("trace", []),
        )
