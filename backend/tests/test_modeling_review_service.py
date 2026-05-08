from uuid import uuid4

import pytest

from app.models.modeling import ModelingJob, ModelingJobStatus, ReviewedModelingResult, ReviewStatus
from app.schemas.modeling import ReviewedModelingResultCreate, WorkflowEventCreate
from app.schemas.review import ReviewResultRequest
from app.services.review.modeling_review_service import ModelingReviewError, ModelingReviewService


class FakeReviewRepository:
    def __init__(self) -> None:
        self.job = ModelingJob(
            id=uuid4(),
            game_name="Baldur's Gate 3",
            steam_url="https://store.steampowered.com/app/1086940/Baldurs_Gate_3/",
        )
        self.reviewed_result = None
        self.events: list[WorkflowEventCreate] = []

    def get_job(self, job_id):
        if job_id == self.job.id:
            return self.job
        return None

    def get_reviewed_result(self, job_id):
        return self.reviewed_result

    def save_reviewed_result(self, job: ModelingJob, data: ReviewedModelingResultCreate):
        self.reviewed_result = ReviewedModelingResult(
            id=uuid4(),
            job_id=job.id,
            reviewed_tags=data.reviewed_tags,
            review_status=data.review_status,
            reviewer_notes=data.reviewer_notes,
        )
        return self.reviewed_result

    def update_job_status(self, job: ModelingJob, status: ModelingJobStatus):
        job.status = status
        return job

    def add_workflow_event(self, job: ModelingJob, data: WorkflowEventCreate):
        self.events.append(data)
        return data


def _review_request() -> ReviewResultRequest:
    return ReviewResultRequest(
        reviewed_tags=[
            {
                "tag_code": "combat",
                "weight": 4,
                "confidence": 0.9,
                "evidence_snippets": [{"en": "Fast combat.", "zh": "Fast combat zh."}],
                "reason": {"en": "Combat is central.", "zh": "Combat is central zh."},
            }
        ],
        review_status=ReviewStatus.APPROVED,
        reviewer_notes="Looks good.",
    )


def test_submit_review_saves_reviewed_result_and_updates_job_status() -> None:
    repository = FakeReviewRepository()
    service = ModelingReviewService(repository)

    response = service.submit_review(repository.job.id, _review_request())

    assert response.job_id == repository.job.id
    assert response.review_status == ReviewStatus.APPROVED
    assert repository.job.status == ModelingJobStatus.APPROVED
    assert repository.reviewed_result.reviewed_tags["tags"][0]["tag_code"] == "combat"
    assert repository.events[0].event_type == "review_approved"


def test_export_grs_payload_requires_approved_review() -> None:
    repository = FakeReviewRepository()
    repository.reviewed_result = ReviewedModelingResult(
        id=uuid4(),
        job_id=repository.job.id,
        reviewed_tags={"tags": [{"tag_code": "combat", "weight": 4}]},
        review_status=ReviewStatus.NEEDS_REVIEW,
    )
    service = ModelingReviewService(repository)

    with pytest.raises(ModelingReviewError):
        service.export_grs_payload(repository.job.id)


def test_review_request_rejects_needs_review_status() -> None:
    with pytest.raises(ValueError):
        ReviewResultRequest(
            reviewed_tags=[
                {
                    "tag_code": "combat",
                    "weight": 4,
                }
            ],
            review_status=ReviewStatus.NEEDS_REVIEW,
        )


def test_export_grs_payload_returns_grs_compatible_shape() -> None:
    repository = FakeReviewRepository()
    service = ModelingReviewService(repository)
    service.submit_review(repository.job.id, _review_request())

    payload = service.export_grs_payload(repository.job.id)

    assert payload.model_dump() == [
        {
            "game_code": "baldurs_gate_3",
            "tag_code": "combat",
            "weight": 4,
        }
    ]
    assert repository.job.status == ModelingJobStatus.EXPORTED
    assert repository.reviewed_result.review_status == ReviewStatus.EXPORTED
    assert repository.events[-1].event_type == "exported"
    assert repository.events[-1].payload["grs_payload"] == payload.model_dump()


def test_export_game_code_falls_back_to_game_name_when_steam_slug_is_missing() -> None:
    repository = FakeReviewRepository()
    repository.job.game_name = "Life is Strange"
    repository.job.steam_url = "https://store.steampowered.com/app/319630/"
    service = ModelingReviewService(repository)
    service.submit_review(repository.job.id, _review_request())

    payload = service.export_grs_payload(repository.job.id)

    assert payload.model_dump()[0]["game_code"] == "life_is_strange"


def test_export_game_code_falls_back_to_steam_app_id_when_slug_and_name_are_not_ascii() -> None:
    repository = FakeReviewRepository()
    repository.job.game_name = "漫威争锋"
    repository.job.steam_url = "https://store.steampowered.com/app/2767030/_/"
    service = ModelingReviewService(repository)
    service.submit_review(repository.job.id, _review_request())

    payload = service.export_grs_payload(repository.job.id)

    assert payload.model_dump()[0]["game_code"] == "steam_app_2767030"
