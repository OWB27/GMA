from uuid import UUID

from pydantic import BaseModel, Field, RootModel, field_validator

from app.models.modeling import ReviewStatus


ALLOWED_REVIEW_SUBMIT_STATUSES = {
    ReviewStatus.APPROVED,
    ReviewStatus.REJECTED,
}


class ReviewedTagInput(BaseModel):
    tag_code: str = Field(min_length=1)
    weight: int = Field(ge=1, le=5)
    confidence: float | None = Field(default=None, ge=0, le=1)
    evidence_snippets: list[dict[str, str]] = Field(default_factory=list)
    reason: dict[str, str] | None = None


class ReviewResultRequest(BaseModel):
    reviewed_tags: list[ReviewedTagInput] = Field(min_length=1)
    review_status: ReviewStatus = ReviewStatus.APPROVED
    reviewer_notes: str | None = Field(default=None, max_length=5000)

    @field_validator("review_status")
    @classmethod
    def review_status_must_be_review_decision(cls, value: ReviewStatus) -> ReviewStatus:
        if value not in ALLOWED_REVIEW_SUBMIT_STATUSES:
            raise ValueError("review_status must be either approved or rejected.")
        return value


class ReviewResultResponse(BaseModel):
    job_id: UUID
    review_status: ReviewStatus
    reviewed_tags: list[ReviewedTagInput]
    reviewer_notes: str | None


class GRSGameTagExport(BaseModel):
    game_code: str = Field(min_length=1)
    tag_code: str = Field(min_length=1)
    weight: int = Field(ge=1, le=5)


class GRSExportPayload(RootModel[list[GRSGameTagExport]]):
    pass
