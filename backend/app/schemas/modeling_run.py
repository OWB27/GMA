from typing import Any

from pydantic import BaseModel


class ModelingRunResponse(BaseModel):
    job_id: str | None
    game_name: str
    steam_url: str
    source_bundle: dict[str, Any] | None
    source_assessment: dict[str, Any] | None = None
    retrieved_context: dict[str, Any] | None
    modeling_result: dict[str, Any] | None
    validation_result: dict[str, Any] | None
    status: str
    errors: list[str]
    trace: list[dict[str, Any]]
