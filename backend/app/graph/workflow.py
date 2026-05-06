from langgraph.graph import END, START, StateGraph

from app.graph.nodes import (
    collect_sources_node,
    collect_sources_mock_node,
    finish_node,
    model_game_tags_mock_node,
    retrieve_grs_context_node,
    retrieve_grs_context_mock_node,
    start_node,
    validate_result_mock_node,
)
from app.graph.state import GMAGraphState, create_initial_state


def build_mock_workflow():
    graph_builder = StateGraph(GMAGraphState)

    graph_builder.add_node("start", start_node)
    graph_builder.add_node("collect_sources_mock", collect_sources_mock_node)
    graph_builder.add_node("retrieve_grs_context_mock", retrieve_grs_context_mock_node)
    graph_builder.add_node("model_game_tags_mock", model_game_tags_mock_node)
    graph_builder.add_node("validate_result_mock", validate_result_mock_node)
    graph_builder.add_node("finish", finish_node)

    graph_builder.add_edge(START, "start")
    graph_builder.add_edge("start", "collect_sources_mock")
    graph_builder.add_edge("collect_sources_mock", "retrieve_grs_context_mock")
    graph_builder.add_edge("retrieve_grs_context_mock", "model_game_tags_mock")
    graph_builder.add_edge("model_game_tags_mock", "validate_result_mock")
    graph_builder.add_edge("validate_result_mock", "finish")
    graph_builder.add_edge("finish", END)

    return graph_builder.compile()


def build_source_collection_workflow():
    graph_builder = StateGraph(GMAGraphState)

    graph_builder.add_node("start", start_node)
    graph_builder.add_node("collect_sources", collect_sources_node)
    graph_builder.add_node("retrieve_grs_context", retrieve_grs_context_node)
    graph_builder.add_node("model_game_tags_mock", model_game_tags_mock_node)
    graph_builder.add_node("validate_result_mock", validate_result_mock_node)
    graph_builder.add_node("finish", finish_node)

    graph_builder.add_edge(START, "start")
    graph_builder.add_edge("start", "collect_sources")
    graph_builder.add_edge("collect_sources", "retrieve_grs_context")
    graph_builder.add_edge("retrieve_grs_context", "model_game_tags_mock")
    graph_builder.add_edge("model_game_tags_mock", "validate_result_mock")
    graph_builder.add_edge("validate_result_mock", "finish")
    graph_builder.add_edge("finish", END)

    return graph_builder.compile()


def run_mock_workflow(
    game_name: str,
    steam_url: str,
    job_id: str | None = None,
) -> GMAGraphState:
    workflow = build_mock_workflow()
    initial_state = create_initial_state(game_name=game_name, steam_url=steam_url, job_id=job_id)
    return workflow.invoke(initial_state)


def run_source_collection_workflow(
    game_name: str,
    steam_url: str,
    job_id: str | None = None,
) -> GMAGraphState:
    workflow = build_source_collection_workflow()
    initial_state = create_initial_state(game_name=game_name, steam_url=steam_url, job_id=job_id)
    return workflow.invoke(initial_state)
