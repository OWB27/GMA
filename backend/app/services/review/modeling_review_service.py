"""Human review and GRS export use cases for completed modeling runs."""

from uuid import UUID
from urllib.parse import urlparse

from app.models.modeling import ModelingJobStatus, ReviewStatus
from app.repositories.modeling_job_repository import ModelingJobRepository
from app.schemas.modeling import ReviewedModelingResultCreate, WorkflowEventCreate
from app.schemas.review import GRSExportPayload, ReviewResultRequest, ReviewResultResponse


class ModelingReviewError(ValueError):
    """Raised when a review or export action cannot be completed."""

    pass


class ModelingReviewService:
    """Saves human decisions and exports approved results for GRS import."""

    def __init__(self, repository: ModelingJobRepository) -> None:
        self.repository = repository

    def submit_review(self, job_id: UUID, request: ReviewResultRequest) -> ReviewResultResponse:
        job = self.repository.get_job(job_id)
        if job is None:
            raise ModelingReviewError(f"Modeling job not found: {job_id}")

        reviewed_tags_payload = {
            "tags": [tag.model_dump() for tag in request.reviewed_tags],
        }
        reviewed_result = self.repository.save_reviewed_result(
            job=job,
            data=ReviewedModelingResultCreate(
                reviewed_tags=reviewed_tags_payload,
                review_status=request.review_status,
                reviewer_notes=request.reviewer_notes,
            ),
        )
        self.repository.update_job_status(job, self._job_status_for_review(request.review_status))
        self.repository.add_workflow_event(
            job=job,
            data=WorkflowEventCreate(
                event_type=f"review_{request.review_status.value}",
                message="Human review result saved.",
                payload={"reviewed_result_id": str(reviewed_result.id)},
            ),
        )

        return ReviewResultResponse(
            job_id=job.id,
            review_status=reviewed_result.review_status,
            reviewed_tags=request.reviewed_tags,
            reviewer_notes=reviewed_result.reviewer_notes,
        )

    def export_grs_payload(self, job_id: UUID) -> GRSExportPayload:
        job = self.repository.get_job(job_id)
        if job is None:
            raise ModelingReviewError(f"Modeling job not found: {job_id}")

        reviewed_result = self.repository.get_reviewed_result(job_id)
        if reviewed_result is None:
            raise ModelingReviewError("Reviewed modeling result is required before export.")

        if reviewed_result.review_status not in {ReviewStatus.APPROVED, ReviewStatus.EXPORTED}:
            raise ModelingReviewError("Only approved reviewed results can be exported.")

        reviewed_tags = reviewed_result.reviewed_tags.get("tags", [])
        payload = GRSExportPayload(
            [
                {
                    "game_code": self._game_code_from_job(job.game_name, job.steam_url),
                    "tag_code": tag["tag_code"],
                    "weight": tag["weight"],
                }
                for tag in reviewed_tags
            ]
        )

        self.repository.update_job_status(job, ModelingJobStatus.EXPORTED)
        self.repository.save_reviewed_result(
            job=job,
            data=ReviewedModelingResultCreate(
                reviewed_tags=reviewed_result.reviewed_tags,
                review_status=ReviewStatus.EXPORTED,
                reviewer_notes=reviewed_result.reviewer_notes,
            ),
        )
        self.repository.add_workflow_event(
            job=job,
            data=WorkflowEventCreate(
                event_type="exported",
                message="GRS-compatible export payload generated.",
                payload={
                    "grs_payload": payload.model_dump(),
                    "gma_job_id": str(job.id),
                    "reviewed_result_id": str(reviewed_result.id),
                },
            ),
        )

        return payload

    def _game_code_from_job(self, game_name: str, steam_url: str) -> str:
        parsed_url = urlparse(steam_url)
        path_parts = [part for part in parsed_url.path.split("/") if part]
        if len(path_parts) >= 3 and path_parts[0] == "app":
            return self._slugify(path_parts[2])
        return self._slugify(game_name)

    def _slugify(self, value: str) -> str:
        normalized_chars: list[str] = []
        previous_was_separator = False
        for char in value.lower():
            if char.isalnum():
                normalized_chars.append(char)
                previous_was_separator = False
            elif not previous_was_separator:
                normalized_chars.append("_")
                previous_was_separator = True

        return "".join(normalized_chars).strip("_")

    def _job_status_for_review(self, review_status: ReviewStatus) -> ModelingJobStatus:
        if review_status == ReviewStatus.APPROVED:
            return ModelingJobStatus.APPROVED
        if review_status == ReviewStatus.REJECTED:
            return ModelingJobStatus.REJECTED
        raise ModelingReviewError("review_status must be either approved or rejected.")
