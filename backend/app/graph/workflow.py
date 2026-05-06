"""LangGraph workflow for a single GMA modeling run."""

from langgraph.graph import END, START, StateGraph

from app.graph.nodes import (
    collect_sources_node,
    finish_node,
    model_game_tags_node,
    retrieve_grs_context_node,
    start_node,
    validate_result_node,
)
from app.graph.state import GMAGraphState, create_initial_state


def route_after_modeling(state: GMAGraphState) -> str:
    if state["status"] == "failed":
        return "finish"
    return "validate_result"


def build_modeling_workflow():
    """Build the source -> context -> model -> validate workflow graph."""
    graph_builder = StateGraph(GMAGraphState)

    graph_builder.add_node("start", start_node)
    graph_builder.add_node("collect_sources", collect_sources_node)
    graph_builder.add_node("retrieve_grs_context", retrieve_grs_context_node)
    graph_builder.add_node("model_game_tags", model_game_tags_node)
    graph_builder.add_node("validate_result", validate_result_node)
    graph_builder.add_node("finish", finish_node)

    graph_builder.add_edge(START, "start")
    graph_builder.add_edge("start", "collect_sources")
    graph_builder.add_edge("collect_sources", "retrieve_grs_context")
    graph_builder.add_edge("retrieve_grs_context", "model_game_tags")
    graph_builder.add_conditional_edges(
        "model_game_tags",
        route_after_modeling,
        {
            "validate_result": "validate_result",
            "finish": "finish",
        },
    )
    graph_builder.add_edge("validate_result", "finish")
    graph_builder.add_edge("finish", END)

    return graph_builder.compile()


def run_modeling_workflow(
    game_name: str,
    steam_url: str,
    job_id: str | None = None,
) -> GMAGraphState:
    workflow = build_modeling_workflow()
    initial_state = create_initial_state(game_name=game_name, steam_url=steam_url, job_id=job_id)
    return workflow.invoke(initial_state)
