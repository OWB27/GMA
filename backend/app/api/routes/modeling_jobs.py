from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.graph.workflow import run_source_collection_workflow
from app.repositories.modeling_job_repository import ModelingJobRepository
from app.schemas.modeling import ModelingJobCreate
from app.schemas.workflow import RunMockWorkflowResponse
from app.services.modeling_job.modeling_job_service import ModelingJobService

router = APIRouter(prefix="/modeling-jobs", tags=["modeling-jobs"])


@router.post("/run", response_model=RunMockWorkflowResponse)
def create_and_run_modeling_job_route(
    request: ModelingJobCreate,
    session: Session = Depends(get_session),
) -> RunMockWorkflowResponse:
    service = ModelingJobService(
        repository=ModelingJobRepository(session),
        workflow_runner=run_source_collection_workflow,
    )
    result = service.create_and_run_job(request)
    return RunMockWorkflowResponse(**result)
