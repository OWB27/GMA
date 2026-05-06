from typing import Any, TypedDict


class GMAGraphState(TypedDict):
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


def create_initial_state(
    game_name: str,
    steam_url: str,
    job_id: str | None = None,
) -> GMAGraphState:
    return {
        "job_id": job_id,
        "game_name": game_name,
        "steam_url": steam_url,
        "source_bundle": None,
        "retrieved_context": None,
        "modeling_result": None,
        "validation_result": None,
        "status": "created",
        "errors": [],
        "trace": [],
    }
