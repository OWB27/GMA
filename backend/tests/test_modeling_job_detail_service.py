from uuid import uuid4

import pytest

from app.models.modeling import ModelingDraft, ModelingJob, ModelingJobStatus, SourceBundle, WorkflowEvent
from app.services.modeling_run.modeling_job_detail_service import ModelingJobDetailService, ModelingJobNotFoundError


class FakeModelingJobRepository:
    def __init__(self) -> None:
        self.job = ModelingJob(
            id=uuid4(),
            game_name="Hades",
            steam_url="https://store.steampowered.com/app/1145360/Hades/",
            status=ModelingJobStatus.NEEDS_REVIEW,
        )
        self.source_bundle = SourceBundle(
            job_id=self.job.id,
            raw_data={"short_description": "Mock source."},
        )
        self.modeling_draft = ModelingDraft(
            job_id=self.job.id,
            raw_model_output={"selected_existing_tags": []},
            validation_result={"is_valid": True, "errors": [], "warnings": []},
        )
        self.workflow_event = WorkflowEvent(
            job_id=self.job.id,
            event_type="workflow_finished",
            message="Done.",
            payload={
                "errors": [],
                "trace": [{"node": "finish", "message": "Done."}],
            },
        )

    def get_job(self, job_id):
        if job_id == self.job.id:
            return self.job
        return None

    def get_source_bundle(self, job_id):
        return self.source_bundle

    def get_modeling_draft(self, job_id):
        return self.modeling_draft

    def get_latest_workflow_event(self, job_id, event_type):
        return self.workflow_event


def test_get_job_detail_rebuilds_modeling_run_response() -> None:
    repository = FakeModelingJobRepository()

    response = ModelingJobDetailService(repository).get_job_detail(repository.job.id)

    assert response.job_id == str(repository.job.id)
    assert response.game_name == "Hades"
    assert response.status == "needs_review"
    assert response.source_bundle == {"short_description": "Mock source."}
    assert response.modeling_result == {"selected_existing_tags": []}
    assert response.validation_result == {"is_valid": True, "errors": [], "warnings": []}
    assert response.trace == [{"node": "finish", "message": "Done."}]


def test_get_job_detail_raises_when_job_is_missing() -> None:
    repository = FakeModelingJobRepository()

    with pytest.raises(ModelingJobNotFoundError):
        ModelingJobDetailService(repository).get_job_detail(uuid4())
