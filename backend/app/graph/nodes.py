"""LangGraph nodes for the GMA modeling workflow.

Nodes should stay small: each node updates workflow state by delegating to one
focused service, chain, or validator.
"""

from typing import Any

from app.chains.modeling_chain import ModelingChain
from app.graph.state import GMAGraphState
from app.services.grs_context.grs_context_service import GRSContextService
from app.services.modeling_validation.modeling_result_validator import ModelingResultValidator
from app.services.source_collection.source_collection_service import SourceCollectionService


def append_trace(state: GMAGraphState, node: str, message: str) -> list[dict[str, Any]]:
    return [
        *state["trace"],
        {
            "node": node,
            "message": message,
        },
    ]


def start_node(state: GMAGraphState) -> dict[str, Any]:
    return {
        "status": "started",
        "trace": append_trace(state, "start", "Modeling workflow started."),
    }


def collect_sources_node(state: GMAGraphState) -> dict[str, Any]:
    source_bundle = SourceCollectionService().collect_sources(
        game_name=state["game_name"],
        steam_url=state["steam_url"],
    )

    return {
        "source_bundle": source_bundle.model_dump(),
        "status": "sources_collected",
        "trace": append_trace(
            state,
            "collect_sources",
            "Source bundle collected from Steam official data.",
        ),
    }


def retrieve_grs_context_node(state: GMAGraphState) -> dict[str, Any]:
    retrieved_context = GRSContextService().retrieve_context()

    return {
        "retrieved_context": retrieved_context.model_dump(),
        "status": "context_retrieved",
        "trace": append_trace(state, "retrieve_grs_context", "GRS rule pack context retrieved."),
    }


def model_game_tags_node(state: GMAGraphState) -> dict[str, Any]:
    if state["source_bundle"] is None:
        return {
            "status": "failed",
            "errors": [*state["errors"], "source_bundle is required before modeling."],
            "trace": append_trace(state, "model_game_tags", "Modeling failed because source_bundle is missing."),
        }
    if state["retrieved_context"] is None:
        return {
            "status": "failed",
            "errors": [*state["errors"], "retrieved_context is required before modeling."],
            "trace": append_trace(state, "model_game_tags", "Modeling failed because retrieved_context is missing."),
        }

    try:
        modeling_result = ModelingChain().invoke(
            game_name=state["game_name"],
            steam_url=state["steam_url"],
            source_bundle=state["source_bundle"],
            retrieved_context=state["retrieved_context"],
        )
    except Exception as error:
        return {
            "status": "failed",
            "errors": [*state["errors"], f"model_game_tags failed: {error}"],
            "trace": append_trace(
                state,
                "model_game_tags",
                "Modeling failed during the LLM structured output step.",
            ),
        }

    return {
        "modeling_result": modeling_result.model_dump(),
        "status": "modeled",
        "trace": append_trace(state, "model_game_tags", "Structured modeling result generated."),
    }


def validate_result_node(state: GMAGraphState) -> dict[str, Any]:
    validation_result = ModelingResultValidator().validate(
        modeling_result=state["modeling_result"],
        retrieved_context=state["retrieved_context"],
    )
    status = "validated" if validation_result.is_valid else "validation_failed"
    trace_message = "Modeling result validation passed."
    if not validation_result.is_valid:
        trace_message = "Modeling result validation found errors."
    elif validation_result.warnings:
        trace_message = "Modeling result validation passed with warnings."

    return {
        "validation_result": validation_result.model_dump(),
        "status": status,
        "errors": [*state["errors"], *validation_result.errors],
        "trace": append_trace(state, "validate_result", trace_message),
    }


def finish_node(state: GMAGraphState) -> dict[str, Any]:
    if state["status"] == "failed":
        return {
            "status": state["status"],
            "trace": append_trace(state, "finish", "Workflow finished with failed status."),
        }

    return {
        "status": "finished",
        "trace": append_trace(state, "finish", "Workflow finished."),
    }
