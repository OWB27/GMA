from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.database import get_session
from app.repositories.modeling_job_repository import ModelingJobRepository
from app.schemas.review import GRSExportPayload, ReviewResultRequest, ReviewResultResponse
from app.services.review.modeling_review_service import ModelingReviewError, ModelingReviewService

router = APIRouter(prefix="/modeling-jobs", tags=["modeling-jobs"])


@router.post("/{job_id}/review", response_model=ReviewResultResponse)
def submit_review_route(
    job_id: UUID,
    request: ReviewResultRequest,
    session: Session = Depends(get_session),
) -> ReviewResultResponse:
    service = ModelingReviewService(ModelingJobRepository(session))
    try:
        return service.submit_review(job_id=job_id, request=request)
    except ModelingReviewError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("/{job_id}/export", response_model=GRSExportPayload)
def export_grs_payload_route(
    job_id: UUID,
    session: Session = Depends(get_session),
) -> GRSExportPayload:
    service = ModelingReviewService(ModelingJobRepository(session))
    try:
        return service.export_grs_payload(job_id=job_id)
    except ModelingReviewError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
