"""Application service for creating and running a full modeling job."""

from collections.abc import Callable
from typing import Any

from app.models.modeling import ModelingJobStatus
from app.repositories.modeling_job_repository import ModelingJobRepository
from app.schemas.modeling import (
    ModelingDraftCreate,
    ModelingJobCreate,
    SourceBundleCreate,
    WorkflowEventCreate,
)


WorkflowRunner = Callable[[str, str, str | None], dict[str, Any]]


class ModelingRunService:
    """Runs the full modeling use case and persists the workflow outputs."""

    def __init__(
        self,
        repository: ModelingJobRepository,
        workflow_runner: WorkflowRunner,
    ) -> None:
        self.repository = repository
        self.workflow_runner = workflow_runner

    def create_and_run_job(self, data: ModelingJobCreate) -> dict[str, Any]:
        """Create a job, run the modeling graph, then save the generated artifacts."""
        job = self.repository.create_job(data)
        self.repository.add_workflow_event(
            job=job,
            data=WorkflowEventCreate(
                event_type="job_created",
                message="Modeling job created.",
                payload={"game_name": data.game_name, "steam_url": data.steam_url},
            ),
        )

        workflow_state = self.workflow_runner(data.game_name, data.steam_url, str(job.id))
        self._persist_workflow_state(job=job, workflow_state=workflow_state)
        return workflow_state

    def _persist_workflow_state(self, job, workflow_state: dict[str, Any]) -> None:
        if workflow_state.get("source_bundle") is not None:
            self.repository.save_source_bundle(
                job=job,
                data=SourceBundleCreate(raw_data=workflow_state["source_bundle"]),
            )

        if workflow_state.get("modeling_result") is not None:
            self.repository.save_modeling_draft(
                job=job,
                data=ModelingDraftCreate(
                    raw_model_output=workflow_state["modeling_result"],
                    validation_result=workflow_state.get("validation_result") or {},
                ),
            )

        self.repository.update_job_status(job, self._status_from_workflow(workflow_state))
        self.repository.add_workflow_event(
            job=job,
            data=WorkflowEventCreate(
                event_type="workflow_finished",
                message="Workflow run finished and persisted.",
                payload={
                    "status": workflow_state.get("status"),
                    "errors": workflow_state.get("errors", []),
                    "trace": workflow_state.get("trace", []),
                },
            ),
        )

    def _status_from_workflow(self, workflow_state: dict[str, Any]) -> ModelingJobStatus:
        if workflow_state.get("status") == "failed" or workflow_state.get("errors"):
            return ModelingJobStatus.FAILED
        return ModelingJobStatus.NEEDS_REVIEW
