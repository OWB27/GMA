from uuid import uuid4

from app.models.modeling import ModelingJob, ModelingJobStatus
from app.schemas.modeling import (
    ModelingDraftCreate,
    ModelingJobCreate,
    SourceBundleCreate,
    WorkflowEventCreate,
)
from app.services.modeling_job.modeling_job_service import ModelingJobService


class FakeModelingJobRepository:
    def __init__(self) -> None:
        self.job = None
        self.source_bundle = None
        self.modeling_draft = None
        self.events: list[WorkflowEventCreate] = []

    def create_job(self, data: ModelingJobCreate):
        self.job = ModelingJob(
            id=uuid4(),
            game_name=data.game_name,
            steam_url=data.steam_url,
        )
        return self.job

    def add_workflow_event(self, job: ModelingJob, data: WorkflowEventCreate):
        self.events.append(data)
        return data

    def save_source_bundle(self, job: ModelingJob, data: SourceBundleCreate):
        self.source_bundle = data.raw_data
        return data

    def save_modeling_draft(self, job: ModelingJob, data: ModelingDraftCreate):
        self.modeling_draft = data
        return data

    def update_job_status(self, job: ModelingJob, status: ModelingJobStatus):
        job.status = status
        return job


def test_create_and_run_job_persists_workflow_outputs() -> None:
    repository = FakeModelingJobRepository()

    def workflow_runner(game_name, steam_url, job_id):
        return {
            "job_id": job_id,
            "game_name": game_name,
            "steam_url": steam_url,
            "source_bundle": {"short_description": "Mock source."},
            "retrieved_context": {"allowed_tags": ["combat"]},
            "modeling_result": {"selected_existing_tags": []},
            "validation_result": {"is_valid": True, "errors": [], "warnings": []},
            "status": "finished",
            "errors": [],
            "trace": [{"node": "finish", "message": "Done."}],
        }

    result = ModelingJobService(repository, workflow_runner).create_and_run_job(
        ModelingJobCreate(
            game_name="Hades",
            steam_url="https://store.steampowered.com/app/1145360/Hades/",
        )
    )

    assert result["job_id"] == str(repository.job.id)
    assert repository.source_bundle == {"short_description": "Mock source."}
    assert repository.modeling_draft.raw_model_output == {"selected_existing_tags": []}
    assert repository.job.status == ModelingJobStatus.NEEDS_REVIEW
    assert [event.event_type for event in repository.events] == ["job_created", "workflow_finished"]


def test_create_and_run_job_marks_failed_workflow_as_failed() -> None:
    repository = FakeModelingJobRepository()

    def workflow_runner(game_name, steam_url, job_id):
        return {
            "job_id": job_id,
            "game_name": game_name,
            "steam_url": steam_url,
            "source_bundle": None,
            "retrieved_context": None,
            "modeling_result": None,
            "validation_result": None,
            "status": "failed",
            "errors": ["LLM failed."],
            "trace": [],
        }

    ModelingJobService(repository, workflow_runner).create_and_run_job(
        ModelingJobCreate(
            game_name="Hades",
            steam_url="https://store.steampowered.com/app/1145360/Hades/",
        )
    )

    assert repository.job.status == ModelingJobStatus.FAILED
    assert repository.modeling_draft is None
