from app.graph.nodes import retrieve_grs_context_node
from app.graph.state import create_initial_state
from app.graph.workflow import route_after_modeling, route_after_source_assessment


def test_retrieve_grs_context_node_loads_real_rule_pack() -> None:
    state = create_initial_state(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
    )

    result = retrieve_grs_context_node(state)

    assert result["retrieved_context"]["weight_scale"]["scale"] == "1-5"
    assert len(result["retrieved_context"]["allowed_tags"]) == 20
    assert result["trace"][0]["node"] == "retrieve_grs_context"


def test_route_after_modeling_skips_validation_when_modeling_failed() -> None:
    state = create_initial_state(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
    )
    state["status"] = "failed"

    assert route_after_modeling(state) == "finish"


def test_route_after_modeling_validates_successful_modeling() -> None:
    state = create_initial_state(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
    )
    state["status"] = "modeled"

    assert route_after_modeling(state) == "validate_result"


def test_route_after_source_assessment_finishes_when_assessment_failed() -> None:
    state = create_initial_state(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
    )
    state["status"] = "failed"

    assert route_after_source_assessment(state) == "finish"


def test_route_after_source_assessment_retrieves_context_when_assessment_completes() -> None:
    state = create_initial_state(
        game_name="Hades",
        steam_url="https://store.steampowered.com/app/1145360/Hades/",
    )
    state["status"] = "source_assessed"

    assert route_after_source_assessment(state) == "retrieve_grs_context"
