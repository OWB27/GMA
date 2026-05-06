from fastapi import APIRouter

from app.graph.workflow import run_mock_workflow, run_source_collection_workflow
from app.schemas.workflow import RunMockWorkflowRequest, RunMockWorkflowResponse

router = APIRouter(prefix="/workflow", tags=["workflow"])


@router.post("/run-mock", response_model=RunMockWorkflowResponse)
def run_mock_workflow_route(request: RunMockWorkflowRequest) -> RunMockWorkflowResponse:
    result = run_mock_workflow(
        game_name=request.game_name,
        steam_url=request.steam_url,
    )
    return RunMockWorkflowResponse(**result)


@router.post("/run-source-collection", response_model=RunMockWorkflowResponse)
def run_source_collection_workflow_route(request: RunMockWorkflowRequest) -> RunMockWorkflowResponse:
    result = run_source_collection_workflow(
        game_name=request.game_name,
        steam_url=request.steam_url,
    )
    return RunMockWorkflowResponse(**result)
