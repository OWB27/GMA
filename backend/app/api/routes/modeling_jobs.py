from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.graph.workflow import run_modeling_workflow
from app.repositories.modeling_job_repository import ModelingJobRepository
from app.schemas.modeling import ModelingJobCreate
from app.schemas.modeling_run import ModelingRunResponse
from app.services.modeling_run.modeling_run_service import ModelingRunService

router = APIRouter(prefix="/modeling-jobs", tags=["modeling-jobs"])


@router.post("/run", response_model=ModelingRunResponse)
def create_and_run_modeling_job_route(
    request: ModelingJobCreate,
    session: Session = Depends(get_session),
) -> ModelingRunResponse:
    service = ModelingRunService(
        repository=ModelingJobRepository(session),
        workflow_runner=run_modeling_workflow,
    )
    result = service.create_and_run_job(request)
    return ModelingRunResponse(**result)
