from typing import Any

from pydantic import BaseModel, Field


class RunMockWorkflowRequest(BaseModel):
    game_name: str = Field(min_length=1, max_length=255)
    steam_url: str = Field(min_length=1, max_length=2048)


class RunMockWorkflowResponse(BaseModel):
    job_id: str | None
    game_name: str
    steam_url: str
    source_bundle: dict[str, Any] | None
    retrieved_context: dict[str, Any] | None
    modeling_result: dict[str, Any] | None
    validation_result: dict[str, Any] | None
    status: str
    errors: list[str]
    trace: list[dict[str, Any]]
